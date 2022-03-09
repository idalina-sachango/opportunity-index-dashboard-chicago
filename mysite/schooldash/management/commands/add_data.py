import pandas as pd
from django.core.management.base import BaseCommand
from schooldash.models import cps
from sqlalchemy import create_engine

class Command(BaseCommand):
    help = "Command to add data from a csv file to teh database."

    def handle(self, *args, **options):
        print("Hello world")
        filename = "ncesid-cpsid.csv"
        schools = pd.DataFrame(pd.read_csv(filename))

        schools = schools[["SchoolID", "NCES ID", "Latitude", "Longitude"]]
        schools = schools.fillna(999)
        school_id_ncses_id = schools.astype({"SchoolID": int, "NCES ID": int})

        engine = create_engine("sqlite:///db.sqlite3")

        school_id_ncses_id.to_sql(cps._meta.db_table, if_exists="replace", con=engine, index=True)
