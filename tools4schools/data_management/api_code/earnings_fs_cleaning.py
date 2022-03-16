'''
US Census American Community Survey API Pull

Source: https://www.census.gov/data/developers/guidance/api-user-guide.html

Pulls Census Tract level estimates for
    - Median Earnings
    - Number of Households on Food Stamps
'''
from pathlib import Path
import pandas as pd
import requests



#Census Data
#Household Income: Estimated median earnings in 2017 inflation-adjusted dollars
#Food Stamps: Total estimated households receiving Food Stamps/SNAP
# in past 12 months (2017)
home_path = Path(__file__).parent.parent.parent
data_path = home_path.joinpath("data/economic")

HOST_NAME = "https://api.census.gov/data"
YEAR = "/2017"
DATASET = "/acs/acs5"
ACCESS = "?get="
VARIABLES = "NAME,B22001_002E,B18140_001E"
GEOGRAPHY = "&for=tract:*&in=state:17"

BASE_URL = HOST_NAME + YEAR + DATASET + ACCESS + VARIABLES + GEOGRAPHY
r = requests.get(BASE_URL)
col_names = ["name", "food_stamps", "median_earnings", "state", "county",
            "tract"]
census_df = pd.DataFrame(columns=col_names, data=r.json()[1:])
census_df = census_df.astype({"name": str, "state": str,"county": str,
                "tract": str, "median_earnings": int, "food_stamps": int})
census_df.to_csv(data_path.joinpath("income_food_stamps.csv"), index=False)
