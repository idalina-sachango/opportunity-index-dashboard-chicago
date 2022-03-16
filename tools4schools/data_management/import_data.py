#Nivedita Vatsa
#Import and merge datasets

import pandas as pd
#from tabulate import tabulate
import csv

school_char = pd.read_csv ("C:/Users/nived/OneDrive - The University of Chicago/Academic/Winter 2021/CS 122/Project/Data/_Urban Institute/school_char_by_school_IL_recentyr/EducationDataPortal_02.25.2022_Schools.csv")
demographics = pd.read_csv("C:/Users/nived/OneDrive - The University of Chicago\Academic\Winter 2021/CS 122/Project/Data/_Urban Institute/demographics_by_school_IL_recentyr/EducationDataPortal_02.25.2022_Schools.csv")


joined = pd.merge(school_char, demographics, on = ["ncessch"])

#joined = school_char.join(demographics.set_index(["ncessch"]), lsfuffix = "_char", rsuffix = "_demo", on = ["ncessch"])