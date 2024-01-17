import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import pandas as pd
from scipy.sparse import hstack
import os

# This file stores all data cleaning methods, which are all called by the method at the bottom of the file cleanData()

# Creates binary outcome variable based off of eArrest.18
def createOutcomeColumn(df):
    outcome_mapping = {
        'Expired in ED': 'Dead',
        'Expired in the Field': 'Dead',
        'Ongoing Resuscitation in ED': 'Unknown',
        'ROSC in the Field': 'Alive',
        'ROSC in the ED': 'Alive',
        'Ongoing Resuscitation by Other EMS': 'Unknown'
    }
    df['Outcome'] = df['eArrest_18'].map(outcome_mapping).fillna('Unknown')
    return df


# Imputes the most frequent values for categorical variables and median values for numeric variables
def transformColumnsMedianImputation(df):

    #List of variables we determined were categorical
    potentialCategoricalFeatures = [
    'USCensusRegion', 'eVitals_31', 'eVitals_30', 'eVitals_29', 'eVitals_27', 'eVitals_26',
    'eVitals_21', 'eVitals_20', 'eVitals_19', 'eVitals_08', 'eVitals_04', 'eSituation_13',
    'eSituation_08', 'eSituation_07', 'eSituation_02', 'eScene_09', 'eScene_08', 'eScene_07',
    'eScene_01', 'eResponse_24', 'eResponse_23', 'eResponse_15', 'eResponse_12', 'eResponse_11',
    'eResponse_10', 'eResponse_09', 'eResponse_08', 'eResponse_07', 'eResponse_05', 'eProtocol_02',
    'eProtocol_01', 'eProcedures_10', 'eProcedures_08', 'eProcedures_06', 'eProcedures_03',
    'eProcedures_02', 'ePayment_50', 'ePayment_01', 'ePatient_16', 'ePatient_14', 'ePatient_13',
    'eOutcome_02', 'eOutcome_01', 'eOther_05', 'eMedications_10', 'eMedications_07', 'eMedications_06',
    'eMedications_05', 'eMedications_03', 'eMedications_02', 'eInjury_03', 'eInjury_01', 'eHistory_17',
    'eHistory_01', 'eDisposition_24', 'eDisposition_23', 'eDisposition_22', 'eDisposition_21', 'eDisposition_20',
    'eDisposition_19', 'eDisposition_18', 'eDisposition_17', 'eDisposition_16', 'eDisposition_12', 'eDispatch_02',
    'eDispatch_01', 'eArrest_18', 'eArrest_17', 'eArrest_16', 'eArrest_12', 'eArrest_11', 'eArrest_09',
    'eArrest_07', 'eArrest_04', 'eArrest_03', 'eArrest_02', 'eArrest_01', 'eArrest_01', 'USCensusDivision',
    'NasemsoRegion', 'Urbanicity', 'PcrKey', 'eArrest_05', 'eSituation_12', 'eSituation_09', 'PcrPatientRaceGroupKey',
    'eVitals_02', 'eSituation_10', 'eInjury_04', 'eSituation_11', 'Outcome', 'eScene_06'
    ]

    # Categorizes the columns of df as categorical or numeric
    numericFeatures = [col for col in df.columns if col not in potentialCategoricalFeatures]
    categoricalFeatures  = [col for col in df.columns if col in potentialCategoricalFeatures]

    print("Numeric features: ", numericFeatures)
    print("Categorical features: ", categoricalFeatures)

    # Loops through numeric features and drops mis-coded data values, then saves column as floats
    for feature in numericFeatures:
        #print(feature)
        df[feature] = df[feature].replace("Not Applicable", pd.NA)
        df[feature] = df[feature].replace("Not Recorded", pd.NA)
        df[feature] = df[feature].replace("No verbal/vocal response (All Age Groups)", pd.NA)
        df[feature] = df[feature].replace("Obeys commands (>2Years); Appropriate response to stimulation", pd.NA)
        df[feature] = df[feature].replace("Incomprehensible sounds (>2 Years); Inconsolable, agitated", pd.NA)
        df[feature] = df[feature].replace("Oriented (>2 Years); Smiles, oriented to sounds, follows objects, interacts", pd.NA)
        df[feature] = df[feature].replace("Confused (>2 Years); Cries but is consolable, inappropriate interactions", pd.NA)
        df[feature] = df[feature].replace("Inappropriate words (>2 Years); Inconsistently consolable, moaning", pd.NA)
        df[feature] = df[feature].astype(dtype='Float64')

    # Sets up pipelines to impute numeric and categorical variables differently, both set to essentially most common value. Then combined pipelines together
    numeric_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))])
    categorical_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy="most_frequent"))])

    preprocessor = ColumnTransformer(transformers=[("num", numeric_transformer, numericFeatures),("cat", categorical_transformer, categoricalFeatures)])
    pipeline = Pipeline(steps=[("preprocessor", preprocessor)])
    pipeline.set_output(transform="pandas")

    # Puts df through the pipeline for imputation 
    result_df = pipeline.fit_transform(df)

    return result_df


# Drops date/time columns. Also drops categorical variables with >100 possible values, as this would break the OneHotEncoding (on my machine) -> may reassess including these variables later
def dropColumns(df):
    features_to_exclude = [
    'eProcedures_01', 'eVitals_01', 'eArrest_14', 'eArrest_15', 'eSituation_01',
    'eTimes_01', 'eTimes_03', 'eTimes_05', 'eTimes_06', 'eTimes_07', 'eTimes_09',
    'eTimes_11', 'eTimes_12', 'eTimes_13', 'eMedications_01', 'PcrMedicationKey', 'eMedications_03Descr',
    'eDisposition_25', 'PcrVitalKey', 'PcrProcedureKey', 'eScene_09', 'eMedications_03', 'eProtocol_01', 'eMedications_05', 'eSituation_12',
    'eSituation_09', 'PcrPatientRaceGroupKey', 'eInjury_01', 'eProcedures_03', 'eSituation_10', 'eSituation_11'
    ]
    df = df.drop(columns=features_to_exclude, errors='ignore')
    return df


# Makes missing value codes NA
def makeMissingValuesNA(df):
    df.replace(7701001, np.nan, inplace=True)
    df.replace(7701003, np.nan, inplace=True)
    df.replace('7701001', np.nan, inplace=True)
    df.replace('7701003', np.nan, inplace=True)
    df.replace('. ', np.nan, inplace=True)
    df.replace('.', np.nan, inplace=True)
    return df


# Encodes categorical variables with OneHotEncoder
def oneHotEncodeCat(X):
    # Identify categorical columns with 'cat__' in the column title
    categorical_columns = [col for col in X.columns if 'cat__' in col and col != 'cat__PcrKey']

    # Create a DataFrame with only categorical columns
    X_cat = X[categorical_columns]

    # Create a DataFrame with non-categorical columns
    X_non_cat = X.drop(columns=categorical_columns)

    # Apply OneHotEncoder to categorical columns
    encoder = OneHotEncoder(sparse_output=True)
    X_cat_encoded = encoder.fit_transform(X_cat)

    # Combine sparse matrix with non-categorical columns
    X_cat_encoded_df = pd.DataFrame.sparse.from_spmatrix(X_cat_encoded, columns=encoder.get_feature_names_out(X_cat.columns))
    X_cat_encoded_df_dense = X_cat_encoded_df.sparse.to_dense()

    # Combine the encoded categorical columns with the non-categorical columns
    X_combined = pd.concat([X_non_cat.reset_index(drop=True), X_cat_encoded_df_dense], axis=1)

    return X_combined


# Scales numeric features with standardscaler
def scaleNum(X):
    numeric_columns = [col for col in X.columns if 'num__' in col and col != 'cat__PcrKey']

    X_num = X[numeric_columns]
    X_non_num = X.drop(columns=numeric_columns)

    # Apply standardScaler to categorical columns
    scaler = StandardScaler()
    X_num_scaled = scaler.fit_transform(X_num)

    X_num_scaled_df = pd.DataFrame(X_num_scaled, columns=X_num.columns)
    X_combined = pd.concat([X_non_num.reset_index(drop=True), X_num_scaled_df], axis=1)

    return X_combined


# Saves a summary of each column to a csv file
def summarizeDF(df, fileName):
    variable_summaries = {}
    # Loop through each column in the DataFrame
    for column in df.columns:
        # Get summary statistics for each column
        summary_stats = df[column].describe(include='all')  # include='all' includes non-numeric data
        
        # Store the summary statistics in the dictionary
        variable_summaries[column] = summary_stats

    # Convert the dictionary to a DataFrame
    summary_df = pd.DataFrame(variable_summaries)

    # Save the variable summaries to a CSV file
    summary_df.to_csv(fileName, index_label='Statistic')



#Saves the value counts for all columns to a txt file
def save_value_counts_to_text(df, output_file):
    if 'PcrKey' in df.columns:
        df.drop(columns=['PcrKey'], inplace=True)
    if 'cat__PcrKey' in df.columns:
        df.drop(columns=['cat__PcrKey'], inplace=True)
    
    with open(output_file, 'w') as file:
        for column in df.columns:
            # Get value counts for each column, including NA values
            value_counts = df[column].value_counts(dropna=False)

            # Write the column name to the file
            file.write(f"Column: {column}\n")

            # Write the value counts to the file
            file.write(value_counts.to_string() + '\n\n')

# Checks if an output folder exists and creates it if not
def create_output_folder(folder_name):
    # Check if the folder exists
    if not os.path.exists(folder_name):
        # If not, create the folder
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")



# Runs all of the above data cleaning steps and saves the file ; the log parameter determines if summary files of the data are savedafter each step, used to debug/understand steps
def cleanData(df, log=False):

    # Add outcome variable, drop rows with missing values in the outcome
    print("Original Data: ", df.shape)
    if log == True:
        create_output_folder('output')
        summarizeDF(df, 'output/summary0Pre.csv')
    #print(df.head)
    #print(type(df))
    #print(df.columns)
    #print(df['eOutcome_01'].value_counts())

    # Create outcome variable
    df = createOutcomeColumn(df)
    print("Target variable added: ", df.shape)
    #print(df.head)
    #print(type(df))
    #print(df.columns)
    if log == True:
        summarizeDF(df, 'output/summary1Outcome.csv')

    # Drop date/time columns
    df = dropColumns(df)
    print("Date/Time features excluded: ", df.shape)
    #print(df.head)
    if log == True:
        summarizeDF(df, 'output/summary2Drop.csv')

    # Replace missing value codes  with NA so imputer registers them as missing
    df= makeMissingValuesNA(df)
    print("Replace missing value codes with N/A: ", df.shape)
    if log == True:
        summarizeDF(df, 'output/summary3NAs.csv')  
        tempDF= df.copy()
        save_value_counts_to_text(tempDF, 'output/value_counts_pre_impute.txt')

    # Imputes missing values with median values
    cleanedDF = transformColumnsMedianImputation(df)
    print("Impute missing values and not recorded values with medians: ", cleanedDF.shape)
    #print(cleanedDF.head)
    if log == True:
        summarizeDF(cleanedDF, 'output/summary4Impute.csv')
        tempDF= cleanedDF.copy()
        save_value_counts_to_text(tempDF, 'output/value_counts_final.txt')

    #Saves final clean daata as cleaned_Data.csv
    cleanedDF.to_csv('data/cleaned_Data.csv', index=False)

    return cleanedDF

