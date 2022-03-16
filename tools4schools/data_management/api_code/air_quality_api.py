'''
Chicago Air Quality for 2016 from the CDC

Source: https://dev.socrata.com/foundry/data.cdc.gov/7vu4-ngxx
'''
from pathlib import Path
from sodapy import Socrata
import pandas as pd



#Air Pollution Data
home_path = Path(__file__).parent.parent.parent
data_path = home_path.joinpath("data/environmental")
client = Socrata("data.cdc.gov", "GebpFrUlDXFeM9T0BR6Y11DIV")
results = client.get("7vu4-ngxx", limit=500000)
results_df = pd.DataFrame.from_records(results)
illinois_air = results_df[results_df["statefips"] == "17"]
chi_county_fips = ["31", "43", "89", "97", "111", "197"]
chi_air = illinois_air[illinois_air["countyfips"].isin(chi_county_fips)]
chi_air.to_csv(data_path.joinpath("chi_air.csv"), index=False)
