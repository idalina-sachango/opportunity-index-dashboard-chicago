import sqlite3
import pandas as pd
import requests



cps = pd.DataFrame(pd.read_csv("ncesid-cpsid.csv"))
cps.set_index("SchoolID")

cps = cps[["SchoolID", "NCES ID"]]
cps = cps.fillna(999)
school_id_ncses_id = cps.astype({"SchoolID": int, "NCES ID": int})
