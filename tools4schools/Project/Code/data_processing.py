'''
CS 30122
Nivedita Vatsa

Consolidate Datasets
'''
import numpy as np
import pandas as pd
import requests
from sklearn.preprocessing import StandardScaler

#Set personal directory
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
 

def scale(dat, var_to_scale, scaling_var, per_unit = 1):
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

    Returns: Nothing. Updates dataframe in place.
    '''
    dat[var_to_scale] = (per_unit * dat[var_to_scale]) / dat[scaling_var]


def impute_w_mean(dat, var_to_impute):
    '''
    Impute missing values with mean value.

    Inputs:
    - dat: A Pandas dataframe
    - var_to_impute: variable for which to impute missing values

    Returns: Nothing.  Updates dataframe in place.
    '''
    consolidated[var_to_impute].fillna((consolidated[var_to_impute].mean()), inplace=True)

# IMPORT: CPS Crosswalk
r = requests.get("https://data.cityofchicago.org/resource/c7jj-qjvh.json")
cps_cw_json = r.json()
cps_cw = pd.DataFrame.from_dict(cps_cw_json, orient='columns')
cps_cw.rename(columns = {'nces_id':'ncessch_num'}, inplace = True)
cps_cw['ncessch'] = cps_cw['ncessch_num'].fillna('').astype(str)
vars_to_keep = ['schoolid', 'schoolname', 'fullname', 'schoolname2',
                    'isbe_name', 'street_number', 'street_direction', 'street_name',
                    'city', 'state', 'zip', 'cps_unit', 'oracleid',
                    'school_category', 'community_area_number', 'community_area', 'geographicarea',
                    'geographic_area_number', 'cook_county_district', 'census_block',
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
#is_unique_id(cps_cw,'ncessch_cps')
print(len(cps_cw['ncessch_cps'].unique()))
print(cps_cw.shape)
#cw = pd.merge(ccd_cw, cps_cw, how = "outer", left_on = 'ncessch', right_on = 'ncessch_cps', indicator = True)
cw = pd.merge(ccd_cw, cps_cw, how = "inner", left_on = 'ncessch', right_on = 'ncessch_cps', indicator = True)
cw.rename(columns = {'_merge':'cps_ccd_cw_merge'}, inplace = True)
#cw_chi = cw[cw['city_cps'] == 'Chicago']
#cw_chi_hs = cw[(cw['school_level'] == 'High' or cw['school_category_cps'] == 'HS')]

# IMPORT: CPS college enrollment data
cps_col_enrl = pd.read_excel(data_dir + "CPS/metrics_collenrollpersist_schoollevel_2021.xlsx", sheet_name = "Enrollment & Persistence", header = 1)
cps_col_enrl = cps_col_enrl[['School ID', 'School Name', 'Graduates.3', 'Enrollments.3', 'Enrollment Pct.3']]
cps_col_enrl.columns = cps_col_enrl.columns.str.rstrip(".3")
cps_col_enrl.rename(columns = {'Graduates':'hs_graduates', 'Enrollments':'college_enrollment', 'Enrollment Pct':'college_enrollment_pct'}, inplace = True)
cps_col_enrl['School ID'] = cps_col_enrl['School ID'].astype(str)

# MERGE: CPS college enrollment data and crosswalks (CCD and CPS)
#is_unique_id(cw,['schoolid_cps'])
print(len(cw['schoolid_cps'].unique()))
print(cw.shape)
#consolidated = pd.merge(cps_col_enrl, cw, how = "left", left_on = "School ID", right_on = "schoolid_cps", indicator = True)
consolidated = pd.merge(cps_col_enrl, cw, how = "inner", left_on = "School ID", right_on = "schoolid_cps", indicator = True)
consolidated.rename(columns = {'_merge':'cw_not_in_cps_col_enrl'}, inplace = True)

#########################################################################
#(sanity check) - SHARE WITH TEAM
consolidated.groupby(["cps_ccd_cw_merge","cw_not_in_cps_col_enrl"]).size()
#########################################################################

# IMPORT: CRDC Data
crdc = pd.read_csv(data_dir + "Urban API (from R)/crdc_data_2017.csv")
crdc['ncessch'] = crdc['ncessch'].astype(str)

print(len(crdc['ncessch'].unique()))
print(crdc.shape)
#consolidated = pd.merge(consolidated, crdc, how = "left", on = "ncessch", indicator = True)
consolidated = pd.merge(consolidated, crdc, how = "inner", on = "ncessch", indicator = True)
consolidated.rename(columns = {'_merge':'crdc_not_matched'}, inplace = True)
consolidated.to_csv(out_dir + 'crdc_ccd_cps.csv', index = False)

# MERGE: American Community Survey Data
acs = pd.read_csv(data_dir + 'ACS/acs_data_1.csv')
acs['tract'] = acs['tract'].apply(lambda x: '{0:0>6}'.format(x))
acs['county'] = acs['county'].apply(lambda x: '{0:0>3}'.format(x))
census_vars = ['state', 'county', 'tract']
acs['census_tract'] = acs[census_vars].apply(lambda row: ''.join(row.values.astype(str)), axis=1)

print(len(acs['census_tract'].unique()))
print(acs.shape)
acs_vars_to_keep = ['tot_hhld', 'internet_rate', 'emp_rate_25_64', 'above_pov_rate', 'census_tract']
#consolidated = pd.merge(consolidated, acs[acs_vars_to_keep], how = "left", left_on = "census_tract_cps", right_on = "census_tract", indicator = True)
consolidated = pd.merge(consolidated, acs[acs_vars_to_keep], how = "inner", left_on = "census_tract_cps", right_on = "census_tract", indicator = True)
consolidated.rename(columns = {'_merge':'acs_not_matched'}, inplace = True)
consolidated.rename(columns = {'tot_hhld':'tot_hhld_census_tract'}, inplace = True)

# MERGE: School budgets
cps_budgets = pd.read_csv(data_dir + 'CPS/cps_budgets_2017.csv')
consolidated['oracleid_cps'] = consolidated['oracleid_cps'].str.rstrip(".0")
#consolidated = pd.merge(consolidated, cps_budgets, how = "left", left_on = "oracleid_cps", right_on = "oracle_id", indicator = True)
consolidated = pd.merge(consolidated, cps_budgets, how = "inner", left_on = "oracleid_cps", right_on = "oracle_id", indicator = True)
consolidated.rename(columns = {'_merge':'cps_budget_not_in_cps_col_enrl'}, inplace = True)

# MERGE: Food stamps
inc_fs = pd.read_csv(data_dir + 'Economic/income_food_stamps.csv')
inc_fs['tract'] = inc_fs['tract'].apply(lambda x: '{0:0>6}'.format(x)) #REPEATED CODE !!!
inc_fs['county'] = inc_fs['county'].apply(lambda x: '{0:0>3}'.format(x))
census_vars = ['state', 'county', 'tract'] 
inc_fs['census_tract'] = inc_fs[census_vars].apply(lambda row: ''.join(row.values.astype(str)), axis=1)

print(len(inc_fs['census_tract'].unique()))
print(inc_fs.shape)
#consolidated = pd.merge(consolidated, inc_fs[['food_stamps', 'median_earnings', 'census_tract']], how = 'left', left_on = 'census_tract_cps', right_on = 'census_tract', indicator = True)
consolidated = pd.merge(consolidated, inc_fs[['food_stamps', 'median_earnings', 'census_tract']], how = 'inner', left_on = 'census_tract_cps', right_on = 'census_tract', indicator = True)
consolidated.rename(columns = {'_merge':'inc_fs_not_matched'}, inplace = True)

# MERGE: Air Quality
aqi = pd.read_csv(data_dir + 'Environmental/chi_air.csv')
aqi['ctfips'] = aqi['ctfips'].astype(str)
aqi = aqi[aqi['date'] == '01JAN2016']

print(len(aqi['ctfips'].unique()))
print(aqi.shape)
#consolidated = pd.merge(consolidated, aqi, how = 'left', left_on = 'census_tract_cps', right_on = 'ctfips', indicator = True)
consolidated = pd.merge(consolidated, aqi, how = 'inner', left_on = 'census_tract_cps', right_on = 'ctfips', indicator = True)
consolidated.rename(columns = {'_merge':'aqi_not_matched'}, inplace = True)

# EXPORT
#consolidated.to_csv(out_dir + 'consolidated.csv', index = False)

# VARIABLE LIST
id_lst = ['School ID', 'School Name', 'ncessch', 'school_id',
    'school_name_x', 'leaid_x', 'street_mailing', 'city_mailing',
    'state_mailing', 'zip_mailing', 'street_location', 'city_location',
    'state_location', 'zip_location', 'latitude_x', 'longitude_x',
    'census_tract_x']

outcome_lst = ['college_enrollment', 'college_enrollment_pct']
scaling_vars = ['hs_graduates', 'enrollment_crdc', 'tot_hhld_census_tract']
ind_lst = ['free_or_reduced_price_lunch', 'teachers_certified_fte_crdc',
           'counselors_fte_crdc', 'law_enforcement_fte_crdc',
           'salaries_crdc', 'enrl_AP_crdc', 'above_pov_rate', 'internet_rate',
           'emp_rate_25_64', 'FY 2017 Ending Budget',
           'food_stamps', 'median_earnings', 'ds_pm_pred']

to_scale_school_level = ['free_or_reduced_price_lunch', 'teachers_certified_fte_crdc',
           'counselors_fte_crdc', 'law_enforcement_fte_crdc',
           'salaries_crdc', 'enrl_AP_crdc','FY 2017 Ending Budget']
to_scale_census_tract = ['food_stamps']
inverse_rel_lst = ['free_or_reduced_price_lunch', 'food_stamps', 'ds_pm_pred'] #law enforcement?

# CONSOLIDATE
consolidated = consolidated[id_lst + scaling_vars + outcome_lst + ind_lst]
consolidated.to_csv(out_dir + 'working_df.csv', index = False)


# SCALE

# Scale school-level variables by school enrollment
for var in to_scale_school_level:
    scale(consolidated, var, 'enrollment_crdc')

# Scale census tract-level variables by the number of households
for var in to_scale_census_tract:
    scale(consolidated, var, 'tot_hhld_census_tract')

# STANDARDIZE
for var in ind_lst:
    impute_w_mean(consolidated, var)
consolidated[ind_lst] = StandardScaler().fit_transform(consolidated[ind_lst])


# ENSURE APPROPRIATE DIRECTIONALITY
for var in inverse_rel_lst:
    consolidated[var] = (-1) * consolidated[var]

# CALCULATE INDEX
consolidated['opportunity_index'] = consolidated[ind_lst].mean(axis=1)
consolidated.to_csv(out_dir + 'working_df.csv', index = False)



# Alignment?
#mvars = ['cps_ccd_cw_merge', 'crdc_not_matched', 'cw_not_in_cps_col_enrl', 'acs_not_matched', 'cps_budget_not_in_cps_col_enrl', 'inc_fs_not_matched', 'aqi_not_matched']
#x = consolidated[['School ID'] + mvars].groupby(mvars).agg(['count'])
#x.to_csv(out_dir + 'alignment.csv', index = True)