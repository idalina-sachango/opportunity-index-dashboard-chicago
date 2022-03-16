# proj-tools4schools
Final Project for CAPP122

# Team
Akila Forde, Dharini Ramaswamy, Idalina Sachango, Nivedita Vatsa

# Description
Our team is interested in exploring inequity in the Chicago school system. Our goal is to develop an index at the school-level that measures a student’s level of opportunity.  We will then compare our constructed index with college enrollment rates to validate our results.  It will consider factors such as school environment, economic hardship, crime, housing security, access to nutrition, access to the internet, and school budget allocation.  We hope that education institutions can utilize our index and analysis to effectively allocate resources and support students’ learning needs. This index is inspired by the Child Opportunity Index 2.0 project.  We intend to follow a similar methodology, but this time, the data (and corresponding weights) will be Chicago-specific.

# To Run package

1. ```bash install.sh``` - will create a virtual environment, load necessary packages and run api data code
2. run ```source env/bin/activate``` - will open the virtual environment
3. run ```python -m tools4schools``` - will run the package
4. Ctrl + Click the url in the terminal


# File Structure

```
- install.sh
- README.md
- requirements
- tools4schools/
    - __init__.py
    - __main__.py
    - app.py
    - assets/
        - style.css
        - style2.css
    - charts/
        - __init__.py
        - enroll_scatter.py
        - scatter.py
        - air_pollution.py
    - data/
        - acs/
            - acs_data_1.csv
        - ccd_crdc/
            - ccd_directory_2017.csv
            - crdc_data_2017.csv
        - cps/
            - cps_budgets_2017.csv
            - metrics_attendance_2021.xlsx
            - metrics_collenrollpersist_schoollevel_2021.xlsx
            - '_READ ME.txt'
            - isbepublicdata_mobility_chronictruancy_2021.xlsx
            - metrics_collenrollpersist_citywide_2021.xlsx
            - raw_budget_data.csv
        - economic/
            - income_food_stamps.csv
        - environmental/
            - chi_air.csv
        - geojson/
            - chicago_boundaries.geojson
            - cps-geojson.geojson
            - census_tract.geojson
            - cps-commarea-bounds.geojson
            - zipcodes.geojson
        - results/
            - consolidated.csv
            - indicators_by_school_per_unit.csv
            - indicators_by_school_scaled.csv
            - indicators_by_school_unscaled.csv
            - opportunity_index_by_school_scaled.csv
    - data_management/
            - acs_api_1.py
            - calculate_index.py
            - data_processing.py
            - import_data.py
            - master.py
            - Untitled.ipynb
            - urban_data_import.R
```

# Example Tools4Schools App Interaction

1. Toggling through Maps
   - Toggle to the College Enrollment map, press the ```College Enrollment Percent by School``` button
   - Hover over the data points to view school name and the Percent college enrollment

2. Filtering by School
    - Scroll down to the DashTable at the bottom
    - Type ```Lane``` and press enter to view consolidated opportunity index and indicators for Lane Technical High School




