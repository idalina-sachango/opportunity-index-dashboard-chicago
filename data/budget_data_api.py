import pandas as pd
import requests
from sodapy import Socrata
import csv 


#CPS Budget Data FY 2017
home_path = Path(__file__).parent.parent 
data_path = home_path.joinpath("data/cps")
school_budgets_df = pd.read_csv("raw_budget_data.csv")
school_budgets_df.drop(school_budgets_df.columns[[2, 4, 5, 6, 7, 8, 9, 10]], axis = 1, inplace = True)
school_budgets_df = school_budgets_df.rename(columns={"Unit": "oracle_id","Unit Name": "school_name"})
school_budgets_df = school_budgets_df.astype({"oracle_id": str, "school_name": str})
school_budgets_df["FY 2017 Ending Budget"] = pd.to_numeric(school_budgets_df["FY 2017 Ending Budget"].str.replace(",",""))
school_budgets_df= school_budgets_df[school_budgets_df["FY 2017 Ending Budget"] != 0]
school_budgets_df.to_csv('/data/cps/cps_budgets_2017.csv', index=False)
