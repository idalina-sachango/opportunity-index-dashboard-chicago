'''
CS 30122
Nivedita Vatsa

Construct class
'''
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from opportunity import Opportunity

#Set directories
data_dir = "../data/"
out_dir = data_dir + "results/"

id_vars = ['School ID', 'School Name', 'ncessch', 'school_id',
    'school_name', 'leaid', 'latitude', 'longitude',
    'census_tract', 'enrollment_crdc']

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


scaler_dict = {"teacher_count": 'teachers_certified_fte_crdc',
               "student_count": "enrollment_crdc",
               "census_households": "tot_hhld_census_tract"}


# instance of Opportunity class
consolidated = pd.read_csv(out_dir + 'consolidated.csv')
Opp = Opportunity(consolidated, id_vars, to_scale_dict, outcome_var, scaler_dict, out_dir)

# export to see what the data look like before processing
Opp.export_df('indicators_by_school_unscaled.csv', keep_ind = True)

# generate opportunity index
Opp.get_opp_index(export = True)