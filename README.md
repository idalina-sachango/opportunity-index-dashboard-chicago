# proj-tools4schools
Final Project for CAPP122

# Team
Akila Forde, Dharini Ramaswamy, Idalina Sachango, Nivedita Vatsa

# Description
In this project, our team explored factors that affect educational inequity in the Chicago public school system. We accomplished this by developing an index that measures a student’s level of opportunity for each school. In calculating our opportunity index, we weighted factors such as internet access, poverty rate, unemployment rate, air pollution, median household earnings and school budget allocation. Our visualizations map the calculated opportunity index, school budget allocation and poverty rate at the census tract level and include distinctions for school size. Additionally, we compared our constructed index with college enrollment rates to validate our results. Our results indicate that the opportunity index is positively correlated with college enrollment rates, meaning that a student’s level of opportunity impacts the likelihood that they will enroll in a four-year college. We hope that education institutions can utilize our index and analysis to effectively allocate resources and support students’ learning needs. This index is inspired by the Child Opportunity Index 2.0 project. We followed a similar methodology and utilized Chicago-specific data and weights.

# To Run package in Linux

1. ```bash install.sh``` - will create a virtual environment, load necessary packages and run api data code
2. run ```source env/bin/activate``` - will open the virtual environment
3. run ```python -m tools4schools``` - will run the package
4. Ctrl + Click the url in the terminal


# Example Tools4Schools App Interaction

1. Toggling through Maps
   - Toggle to the College Enrollment map, press the ```College Enrollment Percent by School``` button
   - Hover over the data points to view school name and the Percent college enrollment

2. Filtering by School
    - Scroll down to the DashTable at the bottom
    - Type ```Lane``` in the dropdown which says 'Filter by School Name' and press enter to view consolidated
        opportunity index and indicators for Lane Technical High School

3. Filter Table by Opportunity Index
    - To view all schools with an Opportunity Index greater than 80.
    - Navigate to the Opportunity Index column and type `> 80` in the input bar
