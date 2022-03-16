'''
CS 30122: tools4schools
Consolidate datasets. Perform cleaning operations
to better harhomize the data sources.
'''
import pandas as pd
import requests

# set directories
data_dir = "../data/"
out_dir = data_dir + "results/"

# helper function
def process_fips(dat):
    '''
    Clean fips data and geneate a new fips code for census tracts.
    Ensure that fips codes are strings of an fixed length. Then
    combine state, county, and tract codes to create a single and
    unique census tract code.

    Inputs:
    - data: A Pandas dataframe

    Returns: Nothing. Updated dataframe in place.
    '''
    fips_len = {'state': '2', 'county': '3', 'tract': '6'}
    for var, target_len in fips_len.items():
        assert var in dat.columns, "{} not in data".format(var)
        set_format = ["{0:0>", target_len, "}"]
        dat[var] = dat[var].apply(lambda x: ''.join(set_format).format(x))
    dat['census_tract'] = dat[fips_len.keys()].apply(lambda row:
                                ''.join(row.values.astype(str)),
                                axis=1)
 

# DATA PROCESSING

# IMPORT: CPS school inventory data; to be used as a crosswalk
r = requests.get("https://data.cityofchicago.org/resource/c7jj-qjvh.json")
cps_cw_json = r.json()
cps_cw = pd.DataFrame.from_dict(cps_cw_json, orient='columns')
cps_cw.rename(columns = {'nces_id':'ncessch_num'}, inplace = True)
cps_cw['ncessch'] = cps_cw['ncessch_num'].fillna('').astype(str)
vars_to_keep = ['schoolid', 'schoolname', 'fullname', 'schoolname2',
                    'isbe_name', 'street_number', 'street_direction',
                    'street_name',
                    'city', 'state', 'zip', 'cps_unit', 'oracleid',
                    'school_category', 'community_area_number',
                    'community_area',
                    'geographicarea',
                    'geographic_area_number', 'cook_county_district',
                    'census_block',
                    'latitude', 'longitude', 'ncessch_num', 'ncessch']
cps_cw = cps_cw[vars_to_keep]
cps_cw['census_tract'] = cps_cw['census_block'].str[:-4]
cps_cw['oracleid'] = cps_cw['oracleid'].str.rstrip(".0")
cps_cw = cps_cw.add_suffix('_cps')


# IMPORT: CCD Directory
ccd_cw = pd.read_csv(data_dir + "ccd_crdc/ccd_directory_2017.csv")
ccd_cw['ncessch'] = ccd_cw['ncessch'].astype(str)

# MERGE: CCD Directory and CPS Data
cw = pd.merge(ccd_cw,
              cps_cw,
              how = "inner",
              left_on = 'ncessch',
              right_on = 'ncessch_cps', indicator = True)
cw.rename(columns = {'_merge':'cps_ccd_cw_merge'}, inplace = True)
clean_rules = {"Hs" : "High School",
               "HS" : "High School",
               "Acad" : "Academy",
               "Schl" : "School",
               "Elem" : "Elementary",
               "Alt" : "Alternative",
               "Agricult" : "Agricultural",
               "Sci" : "Science",
               "Int" : "International"}
clean_rules = {rf'\b{raw}\b': clean for raw, clean in clean_rules.items()}
cw['school_name'].replace(clean_rules, regex=True, inplace = True)


# IMPORT: CPS college enrollment data
cps_col_enrl = pd.read_excel((data_dir
                    + "CPS/metrics_collenrollpersist_schoollevel_2021.xlsx"),
                    sheet_name = "Enrollment & Persistence", header = 1)
cps_col_enrl = cps_col_enrl[['School ID', 'School Name', 'Enrollment Pct.3']]
cps_col_enrl['college_enroll_pct'] = (
        cps_col_enrl.loc[~cps_col_enrl['Enrollment Pct.3'].isin([".", "*"]),
        'Enrollment Pct.3']).astype(float)
cps_col_enrl['college_enroll_pct'].fillna(999, inplace=True)
cps_col_enrl['School ID'] = cps_col_enrl['School ID'].astype(str)


# GENERATE: Consolidated dataset; will form base for further merges
# and MERGE: CPS college enrollment data and crosswalks (from CCD and CPS)
consolidated = pd.merge(cps_col_enrl,
                        cw,
                        how = "inner",
                        left_on = "School ID",
                        right_on = "schoolid_cps", indicator = True)
consolidated.rename(columns = {'_merge':'cw_not_in_cps_col_enrl'},
                    inplace = True)


# MERGE: Consolidated & CRDC Data
crdc = pd.read_csv(data_dir + "ccd_crdc/crdc_data_2017.csv")
crdc['ncessch'] = crdc['ncessch'].astype(str)
consolidated = pd.merge(consolidated,
                        crdc,
                        how = "inner",
                        on = ['leaid', 'ncessch', 'year', 'fips'],
                        indicator = True)
consolidated.rename(columns = {'_merge':'crdc_not_matched'}, inplace = True)

# MERGE: Consolidated & American Community Survey Data
acs = pd.read_csv(data_dir + 'acs/acs_data_1.csv')
process_fips(acs)
acs_vars_to_keep = ['tot_hhld',
                    'internet_rate',
                    'emp_rate_25_64',
                    'above_pov_rate',
                    'census_tract']
consolidated = pd.merge(consolidated,
                        acs[acs_vars_to_keep],
                        how = "inner",
                        left_on = "census_tract_cps",
                        right_on = "census_tract", indicator = True)
consolidated.drop(['census_tract'], axis = 1, inplace = True)
consolidated.rename(columns = {'_merge':'acs_not_matched',
                               'tot_hhld':'tot_hhld_census_tract'}, inplace = True)

# MERGE: Consolidated & CPS School budget data
cps_budgets = pd.read_csv(data_dir + 'cps/cps_budgets_2017.csv')
consolidated['oracleid_cps'] = consolidated['oracleid_cps'].str.rstrip(".0")
consolidated = pd.merge(consolidated,
                        cps_budgets[['oracle_id', 'FY 2017 Ending Budget']],
                        how = "inner",
                        left_on = "oracleid_cps",
                        right_on = "oracle_id", indicator = True)
consolidated.rename(columns = {'_merge':'cps_budget_not_in_cps_col_enrl'},
                    inplace = True)


# MERGE: Consolidated & Food stamp participation
inc_fs = pd.read_csv(data_dir + 'economic/income_food_stamps.csv')
process_fips(inc_fs)
consolidated = pd.merge(consolidated,
                        inc_fs[['food_stamps',
                                'median_earnings',
                                'census_tract']],
                        how = 'inner',
                        left_on = 'census_tract_cps',
                        right_on = 'census_tract', indicator = True)
consolidated.rename(columns = {'_merge':'inc_fs_not_matched'}, inplace = True)


# MERGE: Consolidated & Air Quality Measurements
aqi = pd.read_csv(data_dir + 'environmental/chi_air.csv')
aqi['ctfips'] = aqi['ctfips'].astype(str)
aqi = aqi.groupby(['ctfips'])['ds_pm_pred'].sum().reset_index()
consolidated = pd.merge(consolidated,
                        aqi,
                        how = 'inner',
                        left_on = 'census_tract_cps',
                        right_on = 'ctfips', indicator = True)
consolidated.rename(columns = {'_merge':'aqi_not_matched'}, inplace = True)


# EXPORT: Consolidated data
consolidated.to_csv(out_dir + 'consolidated.csv', index = False)
