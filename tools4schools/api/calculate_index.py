'''
CS 30122
Nivedita Vatsa

Consolidate Datasets
'''
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

#Set directories
data_dir = "../Data/"
out_dir = "../Output/"

consolidated = pd.read_csv(out_dir + 'indicators_by_school_scaled.csv')

# xx: can this be inherited as a class attribute?
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
other 

def get_betas(dat, y_var, x_lst):
    '''
    Get beta coefficients: xx
    '''
    beta_dict = {}
    for x_var in x_lst:
        ols = LinearRegression().fit(dat[[x_var]], 
                                     dat[[y_var]])
        coef = ols.coef_.flatten()
        beta_dict[x_var] = abs(coef)
        beta_dict['total'] = beta_dict.get('total', 0) + abs(coef)
        if coef < 0:
            dat[x_var] = dat[x_var] * (-1)
    return beta_dict


betas = get_betas(consolidated, 'college_enroll_pct', indicator_lst)

consolidated['opportunity_index'] = 0
for var in indicator_lst:
    consolidated['opportunity_index'] += consolidated[var] * (betas[var] / betas['total'])

opportunity_index = consolidated[id_vars + outcome_var + ['opportunity_index']]
opportunity_index.to_csv(out_dir + 'opportunity_index_by_school_scaled.csv', index = False)