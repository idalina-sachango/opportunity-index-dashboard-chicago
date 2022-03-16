import pandas as pd
import requests
from sodapy import Socrata
import csv 


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
census_df = census_df.astype({"name": str, "state": str,"county": str, "tract": str, 
     "median_earnings": int, "food_stamps": int})
#census_df.to_csv("/data/economic/income_food_stamps.csv", index=False)
