'''
CS 30122
Nivedita Vatsa

Construct class
'''
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


class Opportunity():
    '''
    xx
    '''
    def __init__(self, dat, id_vars, to_scale_dict, outcome_var, scaler_dict,
                 out_dir):
        '''
        xx
        '''
        self.dat = dat
        self.id_vars = id_vars
        self.to_scale_dict = to_scale_dict
        self.indicator_lst = sum(list(self.to_scale_dict.values()), [])
        self.outcome_var = outcome_var
        self.scaler_dict = scaler_dict
        self.out_dir = out_dir


    def export_df(self, fname, keep_ind = False, keep_opp_idx = False):
        '''
        xx
        '''
        vars_to_keep = self.id_vars + self.outcome_var
        if keep_ind:
            vars_to_keep += self.indicator_lst
        if keep_opp_idx:
            vars_to_keep.append('opportunity_index')

        to_export = self.dat[vars_to_keep]
        to_export.to_csv(self.out_dir + fname, index = False)

    
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


    def impute_w_mean(self, export = False):
        '''
        Impute missing values with mean value.

        Inputs:
        - dat: A Pandas dataframe
        - vars_to_impute (str): list of var string names to impute

        Returns: Nothing.  Updates dataframe in place.
        '''
        for var in self.indicator_lst:
            self.dat[var].fillna((self.dat[var].mean()), inplace=True)

        if export:
            self.export_df('indicators_by_school_imputed.csv', keep_ind = True)


    def scale_df(self, export = True):
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

        if export:
            self.export_df('indicators_by_school_per_unit.csv', keep_ind = True)


    def standardize_df(self, export = False):
        '''
        xx
        '''
        self.dat[self.indicator_lst] = StandardScaler().fit_transform(
                                        self.dat[self.indicator_lst])

        if export:
            self.export_df('indicators_by_school_scaled.csv', keep_ind = True)

    
    def run_prep_steps(self):
        '''
        '''
        # scale all variables
        self.scale_df(export = True)

        # impute missing values
        self.impute_w_mean(export = False)

        # standardize (mean = 0, sd = 1)
        self.standardize_df(export = True)

        # derive weights
        betas = self.get_betas()

        return betas
    
    
    def get_opp_index(self, export = False):
        '''
        xx
        '''
        beta_dict = self.run_prep_steps()

        self.dat['opportunity_index'] = 0
        for var in self.indicator_lst:
            self.dat['opportunity_index'] += self.dat[var] * (
                                            (beta_dict[var] / 
                                            beta_dict['total']))

        min = self.dat['opportunity_index'].min()
        range = self.dat['opportunity_index'].max() - min
        self.dat['opportunity_index'] = ((self.dat['opportunity_index'] - min)
                                          * (100 / range)).round(2)

        if export:
            self.export_df('opportunity_index_by_school_scaled.csv', keep_ind = False, keep_opp_idx = True)
