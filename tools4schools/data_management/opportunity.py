'''
CS 30122
Nivedita Vatsa

Construct class to house data on student
opportunity. Define methods to construct an
index to measure opportunity.
'''

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


class Opportunity():
    '''
    Opportunity class to analyze school-level data.
    '''
    def __init__(self, dat, id_vars, to_scale_dict, scaler_dict, outcome_var,
                    out_dir = None):
        '''
        Constructor:
        - dat: Pandas dataframe with school-level data
        - id_vars (list of str): Variables that identify the data
        - to_scale_dict: dictionary mapping a scaling specification (str)
            to a list of variables names to scale (str).
        - scaler_dict: Dictionary mapping a scaling specification (str)
            to the name of the corresponding scaling variable (str).
        - outcome_var: Outcome variable (str) to withold from scaling
            and standardization operations
        - out_dir: Directory to export the data
        '''
        self.dat = dat
        self.id_vars = id_vars
        self.to_scale_dict = to_scale_dict
        self.indicator_lst = sum(list(self.to_scale_dict.values()), [])
        self.outcome_var = outcome_var
        self.scaler_dict = scaler_dict
        self.out_dir = out_dir

        vars_used = (self.id_vars +
                     self.outcome_var +
                     self.indicator_lst +
                     list(self.scaler_dict.values()))
        for var in vars_used:
            assert var in self.dat.columns, "{} not in data".format(var)


    def export_df(self, fname, keep_ind = False, keep_opp_idx = False):
        '''
        Export dataset to csv.

        Inputs:
        - fname (str): Name of exported file
        - keep_ind (bool): Indicates whether to export indicator variables
        - keep_opp_indx (bool): Indicates whether to export opportunity index

        Returns: Nothing. Exports a csv.
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
        Calculate the weights for the opportunity index.
        Regress outcome variable on each indicator variable and
        derive a beta coefficient. 

        Inputs: self

        Returns (dict): Dictionary mapping each indicator to a weight.
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
        - export (bool): Indicates whether to export dataframe
            after performing the operation

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
        - self
        - export (bool): Indicates whether to export dataframe
            after performing the operation
        
        Returns: Nothing. Re-scales variables in place.
            Exports csv if specified.
        '''
        for scaler_spec, scaler_var in self.scaler_dict.items():
            for var in self.to_scale_dict[scaler_spec]:
                self.dat[var] = self.dat[var] / self.dat[scaler_var]

        if export:
            self.export_df('indicators_by_school_per_unit.csv', keep_ind = True)


    def standardize_df(self, export = False):
        '''
        Standardizes all indicator variables so that they have a mean
        of 0 and a standard deviation of 1.

        Inupts:
        - self
        - export (bool): Indicates whether to export dataframe
            after performing the operation

        Returns: Nothing. Standardizes variables in place.
            Exports csv if specified.
        '''
        self.dat[self.indicator_lst] = StandardScaler().fit_transform(
                                        self.dat[self.indicator_lst])

        if export:
            self.export_df('indicators_by_school_scaled.csv', keep_ind = True)

    
    def run_prep_steps(self):
        '''
        Execute data preparation steps and calculate weights.

        Input: self

        Returns (dict): Dictionary mapping each indicator to a weight.
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
        Calculate opportunity index.

        Inputs:
        - self
        - export (bool): Indicates whether to export dataframe
            after performing the operation

        Returns: Nothing. Adds column for opportunity index in place.
            Exports csv if specified.
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
