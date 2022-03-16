'''
US Census American Community Survey API Pull

Source: https://www.census.gov/data/developers/guidance/api-user-guide.html

Pulls Census Tract level estimates for
    - Poverty Rate
    - Internet Access
    - Unemployment Rate for Population aged 25-64
'''
from pathlib import Path
import requests
import pandas as pd

home_path = Path(__file__).parent.parent.parent
data_path = home_path.joinpath("data/acs")


census_key = "80ce9e2377354fe9a313a005f010ab4ce8b17b8b"
base_url = 'https://api.census.gov/data/2017/acs/acs5/subject'
cols = 'NAME,S1701_C03_001E,S2801_C01_001E,S2801_C01_012E,S2301_C04_031E'
geo = 'tract:*'
state = '17'

full_url = f'{base_url}?get={cols}&for={geo}&in=state:{state}&key={census_key}'

data_response = requests.get(full_url)
full_json = data_response.json()

df = pd.DataFrame(full_json[1:], columns=full_json[0]).rename(columns={
                                                    "S1701_C03_001E":"pov_rate",
                                                    'S2801_C01_001E':'tot_hhld', 
                                                    'S2801_C01_012E':'tot_hhld_int', 
                                                    'S2301_C04_031E':'unemp_rate_25_64'})

df = df.astype(dtype={"pov_rate":'float64', "tot_hhld":'int64', 
                    "tot_hhld_int":'int64', "unemp_rate_25_64":'float64'})

df = df.assign(internet_rate = 100 * (df.tot_hhld_int / df.tot_hhld),
                emp_rate_25_64 = 100 - df.unemp_rate_25_64,
                above_pov_rate = 100 - df.pov_rate)

df.to_csv(data_path.joinpath('acs_data_1.csv'))
