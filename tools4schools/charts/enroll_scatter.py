
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
from pathlib import Path
import plotly.express as px

home_path = Path(__file__).parent.parent
data_path = home_path.joinpath("data/results")

def make_fig():
    df1 = pd.read_csv(data_path.joinpath("opportunity_index_by_school_scaled.csv"))
    df2 = pd.read_csv(data_path.joinpath('indicators_by_school_unscaled.csv'))

    merged_df = pd.merge(df1[['opportunity_index', 'ncessch', 'enrollment_crdc']], df2, how='left')

    fig = px.scatter(merged_df, x="opportunity_index", y="college_enroll_pct",
                size = "enrollment_crdc", hover_name="school_name", 
                hover_data=["opportunity_index", "college_enroll_pct"],
                labels={
                        "opportunity_index": "School Opportunity Index",
                        "college_enroll_pct": "College Enrollment (%)",
                        "enrollment_crdc": "Number of Certified Full-time Teachers"
                    })
    return fig