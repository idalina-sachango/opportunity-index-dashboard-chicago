'''
CS 30122
Nivedita Vatsa

Consolidate Datasets
'''
from concurrent.futures import process
import numpy as np
import pandas as pd
import requests
import re
from sklearn.preprocessing import StandardScaler

#Set directories
data_dir = "../Data/"
out_dir = "../Output/"

# FUNCTIONS
def is_unique_id(dat, m_var, left_dat):
    '''
    Check whether a dataset is uniquely identified by a set of variables.

    Inputs:
    - dat: A Pandas dataframe
    - m_vars (str): Variable name

    Returns: Nothing. Prints a message indicating whether
    the given dataframe is uniquely identified by the list of
    variable names.
    '''
    num_rows, _ = dat.shape
    num_unique_ids = len(dat[m_var].unique())
    if num_rows == num_unique_ids:
        print("Merging dataset is uniquely identified by merging variables")
    else:
        # val_freq = df.m_var.value_counts()
        # dat[dat.m_var.isin(val_freq.index[val_freq.gt(1)])]

        # val_freq = cps_cw['ncessch_cps'].value_counts()
        # x = cps_cw['ncessch_cps'][cps_cw['ncessch_cps'].isin(val_freq.index[val_freq.gt(1)])].unique()
        # ccd_cw['ncessch'].str.contains(x)
        print("Stop! Merging dataset is NOT uniquely identified by merging variables")
 

def scale_var(dat, var_to_scale, scaling_var, per_unit = 1):
    '''
    Scales a given variable by another variable.  For example,
    the number of students enrolled in the free / reduced-price
    lunch programis scaled by the number of students in the school
    to give the rate of lunch program enrollment.

    Inputs:
    - dat: A Pandas dataframe
    - var_to_scale: variable to scale
    - scaling_var: variable used to scale var_to_scale
    - per_unit: optional argument for scaling per X units
        e.g., when set to 1000, this gives the rate of
        'var_to_scale' per 1000 units of 'scaling_var'.

    Returns: Nothing. Re-scales variable in place.
    '''
    dat[var_to_scale] = (per_unit * dat[var_to_scale]) / dat[scaling_var]


def scale_df(dat, to_scale_dict, scaler_dict):
    '''
    Scale all variables in need of scaling by an appropriate
    scaling variable.

    Inputs:
    - dat: A Pandas dataframe.
    - to_scale_dict: Dictionary mapping a scaling specification
        to a list of variables to scale.
    - scaler_dict: Dictionary mapping a scaling specification
        to a scaling variable.
    
    Returns: Nothing. Re-scales dataframe in place.
    '''
    for scaler_spec, scaler_var in scaler_dict.items():
        for var in to_scale_dict[scaler_spec]:
            scale_var(dat, var, scaler_var)


def impute_w_mean(dat, var_to_impute):
    '''
    Impute missing values with mean value.

    Inputs:
    - dat: A Pandas dataframe
    - var_to_impute (str): variable for which to impute missing values

    Returns: Nothing.  Updates dataframe in place.
    '''
    dat[var_to_impute].fillna((dat[var_to_impute].mean()), inplace=True)


def process_fips(dat):
    '''
    '''
    fips_len = {'state': '2', 'county': '3', 'tract': '6'}
    for var, target_len in fips_len.items():
        set_format = ["{0:0>", target_len, "}"]
        dat[var] = dat[var].apply(lambda x: ''.join(set_format).format(x))
    dat['census_tract'] = dat[fips_len.keys()].apply(lambda row:
                                ''.join(row.values.astype(str)),
                                axis=1)
 
# IMPORT: CPS Crosswalk
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



##########################
#cps_cw.to_csv(out_dir + 'cps_cw.csv', index = False)
##########################


# IMPORT: CCD Directory
ccd_cw = pd.read_csv(data_dir + "Urban API (from R)/ccd_directory_2017.csv")
ccd_cw['ncessch'] = ccd_cw['ncessch'].astype(str)

# MERGE: CCD Directory and CPS 
print(len(cps_cw['ncessch_cps'].unique()))
print(cps_cw.shape)
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
        'Enrollment Pct.3']).astype(float) / 100
cps_col_enrl['college_enroll_pct'].fillna(999, inplace=True)
cps_col_enrl['School ID'] = cps_col_enrl['School ID'].astype(str)

# MERGE: CPS college enrollment data and crosswalks (CCD and CPS)
print(len(cw['schoolid_cps'].unique()))
print(cw.shape)
consolidated = pd.merge(cps_col_enrl,
                        cw,
                        how = "inner",
                        left_on = "School ID",
                        right_on = "schoolid_cps", indicator = True)
consolidated.rename(columns = {'_merge':'cw_not_in_cps_col_enrl'},
                    inplace = True)

#########################################################################
#(sanity check) - SHARE WITH TEAM
consolidated.groupby(["cps_ccd_cw_merge","cw_not_in_cps_col_enrl"]).size()
#########################################################################

# IMPORT: CRDC Data
crdc = pd.read_csv(data_dir + "Urban API (from R)/crdc_data_2017.csv")
crdc['ncessch'] = crdc['ncessch'].astype(str)

print(len(crdc['ncessch'].unique()))
print(crdc.shape)
consolidated = pd.merge(consolidated,
                        crdc,
                        how = "inner",
                        on = ['leaid', 'ncessch', 'year', 'fips'],
                        indicator = True)
consolidated.rename(columns = {'_merge':'crdc_not_matched'}, inplace = True)

# MERGE: American Community Survey Data
acs = pd.read_csv(data_dir + 'ACS/acs_data_1.csv')
process_fips(acs)

print(len(acs['census_tract'].unique()))
print(acs.shape)
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

# MERGE: School budgets
cps_budgets = pd.read_csv(data_dir + 'CPS/cps_budgets_2017.csv')
consolidated['oracleid_cps'] = consolidated['oracleid_cps'].str.rstrip(".0")
consolidated = pd.merge(consolidated,
                        cps_budgets[['oracle_id', 'FY 2017 Ending Budget']],
                        how = "inner",
                        left_on = "oracleid_cps",
                        right_on = "oracle_id", indicator = True)
consolidated.rename(columns = {'_merge':'cps_budget_not_in_cps_col_enrl'}, inplace = True)

# MERGE: Food stamps
inc_fs = pd.read_csv(data_dir + 'Economic/income_food_stamps.csv')
process_fips(inc_fs)
print(len(inc_fs['census_tract'].unique()))
print(inc_fs.shape)
consolidated = pd.merge(consolidated,
                        inc_fs[['food_stamps',
                                'median_earnings',
                                'census_tract']],
                        how = 'inner',
                        left_on = 'census_tract_cps',
                        right_on = 'census_tract', indicator = True)
consolidated.rename(columns = {'_merge':'inc_fs_not_matched'}, inplace = True)


# MERGE: Air Quality
aqi = pd.read_csv(data_dir + 'Environmental/chi_air.csv')
aqi['ctfips'] = aqi['ctfips'].astype(str)
aqi = aqi.groupby(['ctfips'])['ds_pm_pred'].sum().reset_index()


print(len(aqi['ctfips'].unique()))
print(aqi.shape)
consolidated = pd.merge(consolidated,
                        aqi,
                        how = 'inner',
                        left_on = 'census_tract_cps',
                        right_on = 'ctfips', indicator = True)
consolidated.rename(columns = {'_merge':'aqi_not_matched'}, inplace = True)

# MERGE: Crime

# VARIABLE LISTS & DICTIONARIES

id_vars = ['School ID', 'School Name', 'ncessch', 'school_id',
    'school_name', 'leaid', 'latitude', 'longitude',
    'census_tract']

outcome_var = ['college_enroll_pct']
to_scale_dict = {"teacher_count" : ['salaries_crdc'],
                 "student_count" : ['free_or_reduced_price_lunch',
                                    'teachers_certified_fte_crdc',
                                    'counselors_fte_crdc',
                                    'law_enforcement_fte_crdc',
                                    'enrl_AP_crdc',
                                    'FY 2017 Ending Budget'],
                 "census_households": ['food_stamps'],
                 "no_scaling": ['above_pov_rate',
                                'internet_rate',
                                'emp_rate_25_64',
                                'median_earnings',
                                'ds_pm_pred']}

indicator_lst = sum(list(to_scale_dict.values()), [])


scaler_dict = {"teacher_count": 'teachers_certified_fte_crdc',
               "student_count": "enrollment_crdc",
               "census_households": "tot_hhld_census_tract"}

# EXPORT RAW DATA (UNSCALED)
indicators_by_school_unscaled = consolidated[id_vars + outcome_var + indicator_lst]
indicators_by_school_unscaled.to_csv((out_dir +
                                      'indicators_by_school_unscaled.csv'),
                                      index = False)

# SCALE
scale_df(consolidated, to_scale_dict, scaler_dict)

# IMPUTE MISSING VALUES
for var in indicator_lst:
    impute_w_mean(consolidated, var)

# STANDARDIZE
to_std = indicator_lst + outcome_var
consolidated[to_std] = StandardScaler().fit_transform(consolidated[to_std])

# EXPORT RAW DATA (SCALED)
indicators_by_school_scaled = consolidated[id_vars + outcome_var + indicator_lst]
indicators_by_school_scaled.to_csv((out_dir +
                                    'indicators_by_school_scaled.csv'),
                                    index = False)

# CALCULATE INDEX
#consolidated['opportunity_index'] = consolidated[indicator_lst].mean(axis=1)

# EXPORT INDEX
#opportunity_index = consolidated[id_vars + outcome_var + ['opportunity_index']]
#opportunity_index.to_csv(out_dir + 'opportunity_index_by_school_scaled.csv', index = False)



# Alignment?
#mvars = ['cps_ccd_cw_merge', 'crdc_not_matched', 'cw_not_in_cps_col_enrl', 'acs_not_matched', 'cps_budget_not_in_cps_col_enrl', 'inc_fs_not_matched', 'aqi_not_matched']
#x = consolidated[['School ID'] + mvars].groupby(mvars).agg(['count'])
#x.to_csv(out_dir + 'alignment.csv', index = True)