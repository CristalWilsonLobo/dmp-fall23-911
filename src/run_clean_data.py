import pandas as pd
import numpy as np
import data_load.Data_Clean as dc
import sys

# parameter that determines if summary info is saved to text files throughout data cleaning process
# if true, this parameter saves summary stats for each column for each stage in the cleaning process
# and value counts for each variable before and after data imputation
# Parameters not working --> WILL FIX, manually change saveLogs in this file for now
# if len(sys.argv) > 1:
#     saveLogs = sys.argv[1].lower() == 'true'
# else:
#     saveLogs = False
saveLogs = True

# Loads combined data as formatted by the Data_Load.py file from the data directory
print('Creating clean dataset')
df = pd.read_csv('data/combined_data.csv', index_col=False, low_memory=False)
print("Shape of uncleaned data: ", df.shape)


# Cleans and formats data, includiong: imputes values, encodes categorical variables, 
# standardizes continuous variables, creates outcome variable, drops date/time variables
# based on methods in the Clean_Data.py file
df = dc.cleanData(df, saveLogs)


# Prints summary of data
print("Head of dataset and value count of the outcome variable")
print(df['cat__Outcome'].value_counts())
print(df.head)


print('Finished creating cleaned dataset')
