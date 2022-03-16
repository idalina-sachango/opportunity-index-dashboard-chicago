'''
CS 30122
Nivedita Vatsa

Construct class
'''
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

#Set directories
data_dir = "../Data/"
out_dir = "../Output/"

id_vars2 = ['School ID', 'School Name', 'ncessch', 'school_id',
    'school_name', 'leaid', 'latitude', 'longitude',
    'census_tract', 'enrollment_crdc']

outcome_var2 = ['college_enroll_pct']
to_scale_dict2 = {"teacher_count" : ['salaries_crdc'],
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

#indicator_lst2 = sum(list(to_scale_dict.values()), [])


scaler_dict2 = {"teacher_count": 'teachers_certified_fte_crdc',
               "student_count": "enrollment_crdc",
               "census_households": "tot_hhld_census_tract"}

# class SchoolData():
#     '''
#     Consolidated school data
#     '''
#     def __init__(self, dat, to_scale_dict, outcome_var, scaler_dict):
#         '''
#         xx
#         '''
#         self.dat = dat
#         self.to_scale_dict = to_scale_dict
#         self.indicator_lst = sum(list(self.to_scale_dict.values()), [])
#         self.outcome_var = outcome_var
#         self.scaler_dict = scaler_dict



class Opportunity():
    '''
    xx
    '''
    def __init__(self, dat, to_scale_dict, outcome_var, scaler_dict):
        '''
        xx
        '''
        self.dat = dat
        self.to_scale_dict = to_scale_dict
        self.indicator_lst = sum(list(self.to_scale_dict.values()), [])
        self.outcome_var = outcome_var
        self.scaler_dict = scaler_dict


    def get_betas(self):
        '''
        xx
        '''
        beta_dict = {}
        for x_var in self.indicator_lst:
            ols = LinearRegression().fit(self.dat[[x_var]], 
                                        self.dat[self.outcome_var])
            coef = ols.coef_.flatten()
            beta_dict[x_var] = abs(coef)
            beta_dict['total'] = beta_dict.get('total', 0) + abs(coef)
            if coef < 0:
                self.dat[x_var] = self.dat[x_var] * (-1)
        return beta_dict

    def impute_w_mean(self):
        '''
        Impute missing values with mean value.

        Inputs:
        - dat: A Pandas dataframe
        - vars_to_impute (str): list of var string names to impute

        Returns: Nothing.  Updates dataframe in place.
        '''
        for var in self.indicator_lst:
            self.dat[var].fillna((self.dat[var].mean()), inplace=True)

    def scale_df(self):
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
        for scaler_spec, scaler_var in self.scaler_dict.items():
            for var in self.to_scale_dict[scaler_spec]:
                self.dat[var] = self.dat[var] / self.dat[scaler_var]

    def standardize_df(self):
        '''
        xx
        '''
        to_std = self.indicator_lst + self.outcome_var
        self.dat[to_std] = StandardScaler().fit_transform(self.dat[to_std])

    
    def run_all_prep_steps(self):
        '''
        '''
        # scale all variables
        Opp.scale_df()

        # impute missing values
        Opp.impute_w_mean()

        # standardize (mean = 0, sd = 1)
        Opp.standardize_df()

        # derive weights
        betas = Opp.get_betas()

        return betas
    
    
    # def rescale_opp_index(self):
    #     '''
    #     xx
    #     '''
    #     min 
    
    def get_opp_index(self):
        '''
        xx
        '''
        beta_dict = self.run_all_prep_steps()
        
        #if user_provided_wts:

        self.dat['opportunity_index'] = 0
        for var in self.indicator_lst:
            self.dat['opportunity_index'] += self.dat[var] * (
                                            (beta_dict[var] / 
                                            beta_dict['total']))

        min = self.dat['opportunity_index'].min()
        range = self.dat['opportunity_index'].max() - min
        self.dat['opportunity_index'] = ((self.dat['opportunity_index'] - min)
                                          * (100 / range))

        
#school_data_obj = SchoolData(consolidated, to_scale_dict2, outcome_var2, scaler_dict2)
mydata = pd.read_csv(out_dir + 'consolidated.csv')
Opp = Opportunity(mydata, to_scale_dict2, outcome_var2, scaler_dict2)
Opp.get_opp_index()
# #scale
# Opp.scale_df()
# #impute
# Opp.impute_w_mean()
# #standardize
# Opp.standardize_df()
# #get betas
# betas = Opp.get_betas()
# #get index
final_output = mydata[id_vars2 + outcome_var2 + ['opportunity_index']]
print(out_dir)
final_output.to_csv(out_dir + 'opportunity_index_by_school_scaled.csv', index = False)





#mydata['opportunity_index2']

#old_result = pd.read_csv(out_dir + 'opportunity_index_by_school_scaled.csv')
#result['opportunity_index'].head()
