# proj-tools4schools
Final Project for CAPP122

# Team
Akila Forde, Dharini Ramaswamy, Idalina Sachango, Nivedita Vatsa

# Description
Our team is interested in exploring inequity in the Chicago school system. Our goal is to develop an index at the school-level that measures a student’s level of opportunity.  We will then compare our constructed index with college enrollment rates to validate our results.  It will consider factors such as school environment, economic hardship, crime, housing security, access to nutrition, access to the internet, and school budget allocation.  We hope that education institutions can utilize our index and analysis to effectively allocate resources and support students’ learning needs. This index is inspired by the Child Opportunity Index 2.0 project.  We intend to follow a similar methodology, but this time, the data (and corresponding weights) will be Chicago-specific.

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
