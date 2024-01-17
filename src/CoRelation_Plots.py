import pandas as pd
import numpy as np
import os
from lxml import etree
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# Merge primary files "Pub_PCRevents_CA.csv" and "ComputedElements_CA.csv"
def extract_primary_data():

    computedElements_file_path = os.path.abspath("")+"/data/processeddataCA/ComputedElements_CA.csv"
    Pub_PCRevents_file_path = os.path.abspath("")+"/data/processeddataCA/Pub_PCRevents_CA.csv"

    computedElements_dataframe = pd.read_csv(computedElements_file_path, sep=',',  index_col=0, low_memory=False) 
    computedElements_dataframe.dropna(axis=1, how='all', inplace=True)
    print(computedElements_dataframe.head)
    print(computedElements_dataframe.shape)

    pub_PCRevents_dataframe = pd.read_csv(Pub_PCRevents_file_path, sep=',', index_col=0, low_memory=False) 
    pub_PCRevents_dataframe.dropna(axis=1, how='all', inplace=True)
    print(pub_PCRevents_dataframe.head)
    print(pub_PCRevents_dataframe.shape)

    return computedElements_dataframe,pub_PCRevents_dataframe

def combinePrimaryDfs(computedElements_dataframe,pub_PCRevents_dataframe):
    merged_dataframe = computedElements_dataframe.merge(pub_PCRevents_dataframe, on='PcrKey')
    print(merged_dataframe.head())
    print(merged_dataframe.shape)
    return merged_dataframe

def dataframe_stats(df):
    print(df.head)
    print(df.shape)
    df.dropna(axis=1, how='all', inplace=True)

# To read all the files in the processeddataCA folder that have "PCR" keyword in the file name and storing them in a dataframe which are in turn stored in a dictionary that holds all dataframes for each file
# Extracting only PCR related files as we have already extracted ComputedElements_CA and Pub_PCRevents_CA as our primary files, hence used the file pattern as "PCR" to exclude these two files

def extract_data():
    
    directory_path = os.path.abspath("") + "/data/processeddataCA/"
    file_paths = glob.glob(os.path.join(directory_path, "*.csv"))
    dataframes_dict = {}
    excluded_files = ["Pub_PCRevents_CA.csv", "ComputedElements_CA.csv"]

    for file_path in file_paths:
        file_name = os.path.basename(file_path)

        if file_name not in excluded_files:
            print("Storing file", file_name, "in a dataframe")
            df = pd.read_csv(file_path, sep=',', index_col=0, low_memory=False)
            dataframes_dict[file_name] = df
    print("")
    print("The dictionary now holds a list of all files in a dataframe")

    for key, value in dataframes_dict.items():
        print(f"\nFile: {key}")
        print(value.head())

    return dataframes_dict


# To merge all the files in processeddataCA folder stored in above dataframes_dict to our primary dataframe consisting of files ComputedElements_CA and Pub_PCRevents_CA
# Steps : 
# Merging takes place on common column match viz PcrKey
# 
def combineDfs(df_main,df_dict):
    print("Looping through each file in the dataframe dictionary and merging with main dataframe")
    for df_name, df in df_dict.items():
        merged_df = pd.merge(df_main, df, on="PcrKey", how="inner", suffixes=('', '_y'))
        for column in df.columns:
            if "PcrKey" not in column and column not in df_main.columns:
                print("Column ",column,"is not present in main dataframe, hence adding it")
                df_main[column] = merged_df[column]
            elif "PcrKey" not in column:
                print("Column ",column,"is present in main dataframe, checking if all values match with the main dataframe's column")
                column_x = column
                column_y = f"{column}_y"
                merged_df.reset_index(drop=True,inplace=True)
                #merged_df = merged_df.apply(pd.to_numeric, errors='coerce')
                if merged_df[column_x].dtypes == merged_df[column_y].dtypes:
                    #are_equal = ((merged_df[column_x]) == (merged_df[column_y])).all() 
                    are_equal = merged_df[column_x].equals(merged_df[column_y])
                    #match = (merged_df[column_x].apply(pd.to_numeric, errors='coerce')) == (merged_df[column_y].apply(pd.to_numeric, errors='coerce')) 
                #else:
                 #   match = (merged_df[column_x].astype(str) == merged_df[column_y].astype(str))
                    if not are_equal:
                        print("Column ",column,"values does not match with the main dataframe's column, hence adding it to the main dataframe")
                        df_main[column_y] = merged_df[column_y]


    return df_main            
                
    

def load_XSD_Dictionary():

    xsd_directory = os.path.abspath("") + "/data/NEMSIS_XSDs"
    xsd_dicts = {}

    for xsd_filename in os.listdir(xsd_directory):
        if xsd_filename.endswith(".xsd"):
            xsd_path = os.path.join(xsd_directory, xsd_filename)
            xsd_dict = {}
            tree = etree.parse(xsd_path)
            root = tree.getroot()

            for enumeration in root.xpath("//xs:enumeration", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}):
                value = enumeration.get("value")
                documentation = enumeration.find(".//xs:documentation", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"})
                
                if value is not None and documentation is not None:
                    #xsd_dict[value] = documentation.text
                    try:
                        #key = np.int64(value)
                        key = value
                        xsd_dict[key] = documentation.text
                    except ValueError:
                        # Handle the case where 'value' is not a valid int64
                        xsd_dict[value] = documentation.text
                    
            xsd_dict['7701001'] = 'Not Applicable'
            xsd_dict['7701003'] = 'Not Recorded'

            if 'eArrest' in xsd_filename:
                xsd_dict['3011001'] = 'Asystole'
                xsd_dict['3011005'] = 'PEA'
                xsd_dict['3011007'] = 'Unknown AED Non-Shockable Rhythm'
                xsd_dict['3011009'] = 'Unknown AED Shockable Rhythm'
                xsd_dict['3011011'] = 'Ventricular Fibrillation'
                xsd_dict['3011013'] = 'Ventricular Tachycardia-Pulseless'

            if 'ePatient' in xsd_filename:
                xsd_dict['9906001'] = 'Female'
                xsd_dict['9906003'] = 'Male'
                xsd_dict['9906007'] = 'Female-to-Male, Transgender Male'
                xsd_dict['9906009'] = 'Male-to-Female, Transgender Female'
                xsd_dict['9906011'] = 'Other, neither exclusively male or female'
                xsd_dict['9906005'] = 'Unknown (Unable to Determine)'

            if 'eResponse' in xsd_filename:
                xsd_dict['2207011'] = 'Air Transport-Helicopter'
                xsd_dict['2207013'] = 'Air Transport-Fixed Wing'
                xsd_dict['2207015'] = 'Ground Transport (ALS Equipped)'
                xsd_dict['2207017'] = 'Ground Transport (BLS Equipped)'
                xsd_dict['2207019'] = 'Ground Transport (Critical Care Equipped)'
                xsd_dict['2207021'] = 'Non-Transport-Medical Treatment (ALS Equipped)'
                xsd_dict['2207023'] = 'Non-Transport-Medical Treatment (BLS Equipped)'
                xsd_dict['2207025'] = 'Wheel Chair Van/Ambulette'
                xsd_dict['2207027'] = 'Non-Transport-No Medical Equipment'

            if 'eScene01' in xsd_filename:
                xsd_dict['9923001'] = 'No'
                xsd_dict['9923003'] = 'Yes'

            if 'eScene07' in xsd_filename:
                xsd_dict['9923001'] = 'No'
                xsd_dict['9923003'] = 'Yes'

            if 'eSituation02' in xsd_filename:
                xsd_dict['9922001'] = 'No'
                xsd_dict['9922003'] = 'Unknown'
                xsd_dict['9922005'] = 'Yes'
             
            if 'eDisposition23' in xsd_filename:
                xsd_dict['9908001'] = 'Behavioral Health'
                xsd_dict['9908003'] = 'Burn Center'
                xsd_dict['9908005'] = 'Critical Access Hospital'
                xsd_dict['9908007'] = 'Hospital (General)'
                xsd_dict['9908009'] = 'Neonatal Center'
                xsd_dict['9908011'] = 'Pediatric Center'
                xsd_dict['9908019'] = 'Rehab Center'
                xsd_dict['9908021'] = 'Trauma Center Level 1'
                xsd_dict['9908023'] = 'Trauma Center Level 2'
                xsd_dict['9908025'] = 'Trauma Center Level 3'
                xsd_dict['9908027'] = 'Trauma Center Level 4'
                xsd_dict['9908029'] = 'Trauma Center Level 5'
                xsd_dict['9908031'] = 'Cardiac-STEMI/PCI Capable'
                xsd_dict['9908033'] = 'Cardiac-STEMI/PCI Capable (24/7)'
                xsd_dict['9908035'] = 'Cardiac-STEMI/Non-PCI Capable'
                xsd_dict['9908037'] = 'Stroke-Acute Stroke Ready Hospital (ASRH)'
                xsd_dict['9908039'] = 'Stroke-Primary Stroke Center (PSC)'
                xsd_dict['9908041'] = 'Stroke-Thrombectomy-Capable Stroke Center (TSC)'
                xsd_dict['9908043'] = 'Stroke-Comprehensive Stroke Center (CSC)'
                xsd_dict['9908045'] = 'Cancer Center'
                xsd_dict['9908047'] = 'Labor and Delivery'

            xsd_dicts[xsd_filename] = xsd_dict
            print("List of values for variable : ",xsd_filename)
            print(xsd_dict)
            print()
    return xsd_dicts

def updateCodes(merged_dataframe,xsd_dicts):
    for col in merged_dataframe.columns.values:
        matching_xsd_dict = None
        for xsd_name, xsd_dict in xsd_dicts.items():
            xsd_name_modified = xsd_name[1:].split('_')[0]
            #print(xsd_name_modified)
            if xsd_name_modified in col:
                matching_xsd_dict = xsd_dict
                #print("**")
                break

        if matching_xsd_dict:
            #merged_dataframe[col] = merged_dataframe[col].map(lambda x: matching_xsd_dict.get((x), x))
            ####
            #merged_dataframe[col] = merged_dataframe[col].map(matching_xsd_dict).fillna(merged_dataframe[col])
            print("######")
            print(col)
            print(matching_xsd_dict)
            print(merged_dataframe[col])
            print("######")
            #merged_dataframe.replace({col: matching_xsd_dict},inplace=True)
            merged_dataframe[col] = merged_dataframe[col].astype(str).replace(matching_xsd_dict)
            #print(merged_dataframe[col])
    return merged_dataframe


def correlation_matrix(df):
    df_numeric = df.apply(pd.to_numeric, errors='coerce')
    correlation_matrix = df_numeric.set_index(['PcrKey']).corr()
    return correlation_matrix

def scatter_plots(corr,df):
    # Generate scatter plots for the correlated pairs
    for pair in corr.index:
        x, y = pair
        if x != y:
            plt.figure(figsize=(6, 4))
            sns.scatterplot(data=df, x=x, y=y)
            plt.title(f'Scatter Plot for {x} vs {y}')
            plt.xlabel(x)
            plt.ylabel(y)
            plt.show()

if __name__ == '__main__':
    computedElements_dataframe,pub_PCRevents_dataframe = extract_primary_data()
    merged_dataframe = combinePrimaryDfs(computedElements_dataframe,pub_PCRevents_dataframe)
    xsd_dicts = load_XSD_Dictionary()

    dfs_dict = extract_data()
    merged_dataframe = combineDfs(merged_dataframe,dfs_dict)

    ####
    #merged_dataframe = merged_dataframe.apply(pd.to_numeric, errors='ignore')

    merged_dataframe_updated = updateCodes(merged_dataframe,xsd_dicts)
    print(xsd_dicts['eArrest_v3.xsd'])
    print(merged_dataframe_updated.head)
    merged_dataframe_updated.to_csv(os.path.abspath("") + "/data/combined_data.csv", index=False)

    #computedElements_dataframe.drop(columns=computedElements_dataframe.columns[0], axis=1, inplace=True)
    correlation_matrix = correlation_matrix(merged_dataframe_updated)
    print(correlation_matrix)

    # Uncomment below to view co-related pair graphs

    # Find the top 50 highest and lowest correlated pairs
    #top_50_highest_corr = correlation_matrix.unstack().sort_values(ascending=False).head(100)
    #top_50_lowest_corr = correlation_matrix.unstack().sort_values().head(50)

    #print("Top 50 Highest Correlation Pairs:")
    #print(top_50_highest_corr)

    #print("\nTop 50 Lowest Correlation Pairs:")
    #print(top_50_lowest_corr)


    #scatter_plots(top_50_highest_corr,merged_dataframe_updated)
    #scatter_plots(top_50_lowest_corr,merged_dataframe_updated)



