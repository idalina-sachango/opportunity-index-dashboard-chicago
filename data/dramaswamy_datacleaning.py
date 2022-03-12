import pandas as pd
import requests
from sodapy import Socrata
import csv 

#CPS Budget Data FY 2017
school_budgets_df = pd.read_csv("raw_budget_data.csv")
school_budgets_df.drop(school_budgets_df.columns[[2, 4, 5, 6, 7, 8, 9, 10]], axis = 1, inplace = True)
school_budgets_df = school_budgets_df.rename(columns={"Unit": "oracle_id","Unit Name": "school_name"})
school_budgets_df = school_budgets_df.astype({"oracle_id": str, "school_name": str})
school_budgets_df["FY 2017 Ending Budget"] = pd.to_numeric(school_budgets_df["FY 2017 Ending Budget"].str.replace(",",""))
school_budgets_df= school_budgets_df[school_budgets_df["FY 2017 Ending Budget"] != 0]
school_budgets_df.to_csv("cps_budgets_2017.csv", index=False)


#Census Data  
#Household Income: Estimated median earnings in 2017 inflation-adjusted dollars
#Food Stamps: Total estimated households receiving Food Stamps/SNAP in past 12 months (2017)
host_name = "https://api.census.gov/data"
year = "/2017"
dataset = "/acs/acs5"
access = "?get="
variables = "NAME,B22001_002E,B18140_001E"
geography = "&for=tract:*&in=state:17"
base_url = host_name + year + dataset + access + variables + geography
r = requests.get(base_url)
col_names = ["name", "food_stamps", "median_earnings", "state", "county", "tract"]
census_df = pd.DataFrame(columns=col_names, data=r.json()[1:])
census_df = census_df.astype({"name": str, "state": str,"county": str, "tract": str, \
     "median_earnings": int, "food_stamps": int})
census_df.to_csv("income_food_stamps.csv", index=False)


#Air Pollution Data
client = Socrata("data.cdc.gov", "GebpFrUlDXFeM9T0BR6Y11DIV")
results = client.get("7vu4-ngxx", limit=500000)
results_df = pd.DataFrame.from_records(results)
illinois_air = results_df[results_df["statefips"] == "17"]
chi_county_fips = ["31", "43", "89", "97", "111", "197"]
chi_air = illinois_air[illinois_air["countyfips"].isin(chi_county_fips)]
chi_air.to_csv("chi_air.csv", index=False)
