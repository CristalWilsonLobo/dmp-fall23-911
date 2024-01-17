
import os
import glob
import zipfile

# Function to extract .csv files from zip folders
def extract_csv_from_zip(zip_path, target_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

# Specify the main directory where subdirectories containing .plg files and zip folders are located
main_directory = os.path.abspath("")+"/data"

# Create a list to store the file paths
file_paths = []

# Recursively traverse the directory tree
for root, dirs, files in os.walk(main_directory):
    # Use glob to find files with .plg extension in the current directory
    csv_files = glob.glob(os.path.join(root, '*.csv'))
    file_paths.extend(csv_files)
    
    # Use glob to find zip files in the current directory
    zip_files = glob.glob(os.path.join(root, '*.zip'))
    for zip_file in zip_files:
        # Extract .csv files from each zip folder
        extract_csv_from_zip(zip_file, root)
        # Update the list of file_paths with the newly extracted .plg files
        file_paths.extend(glob.glob(os.path.join(root, '*.csv')))

file_paths = [*set(file_paths)]        
print(file_paths)        
print()

# Temporary code 
target_files = [
'FACTPCRDESTINATIONTEAM_CA.csv',
'FACTPCRDESTINATIONREASON_CA.csv',
'FACTPCRCAUSEOFINJURY_CA.csv',
'FACTPCRBARRIERTOCARE_CA.csv',
'FACTPCRARRESTWITNESS_CA.csv',
'FACTPCRARRESTROSC_CA.csv',
'FACTPCRARRESTRHYTHMDESTINATION_CA.csv',
'FACTPCRARRESTRESUSCITATION_CA.csv',
'FACTPCRARRESTCPRPROVIDED_CA.csv',
'FACTPCRALCOHOLDRUGUSEINDICATOR_CA.csv',
'FACTPCRADDITIONALTRANSPORTMODE_CA.csv',
'FACTPCRADDITIONALSYMPTOM_CA.csv',
'FACTPCRADDITIONALRESPONSEMODE_CA.csv',
'ComputedElements_CA.csv'
]
#CA_eID.csv

filtered_file_paths = [filename for filename in file_paths if any(target_file in filename for target_file in target_files)]
print(filtered_file_paths)

target_file_names = {
    'FACTPCRDESTINATIONTEAM_CA.csv':'Destination Team Pre-Arrival Alert or Activation',
'FACTPCRDESTINATIONREASON_CA.csv':'Destination Reason',
'FACTPCRCAUSEOFINJURY_CA.csv':'Cause of Injury',
'FACTPCRBARRIERTOCARE_CA.csv':'Barrier to Care',
'FACTPCRARRESTWITNESS_CA.csv':'Arrest Witness',
'FACTPCRARRESTROSC_CA.csv':'Arrest OSC',
'FACTPCRARRESTRHYTHMDESTINATION_CA.csv':'Arrest Rhythm Destination',
'FACTPCRARRESTRESUSCITATION_CA.csv':'Arrest Resuscitation',
'FACTPCRARRESTCPRPROVIDED_CA.csv':'Arrest CPR Provided',
'FACTPCRALCOHOLDRUGUSEINDICATOR_CA.csv':'Alcohol Drug Use Indicator',
'FACTPCRADDITIONALTRANSPORTMODE_CA.csv':'Additional Transport Mode',
'FACTPCRADDITIONALSYMPTOM_CA.csv':'Additional Symptom',
'FACTPCRADDITIONALRESPONSEMODE_CA.csv':'Additional Response Mode',
'ComputedElements_CA.csv':'Computed Elements'
}

import pandas as pd
import numpy as np
#import dask.dataframe as dd

dfs = {}
for file_path in filtered_file_paths:
    print(f"Processing file: {file_path}")
    dataframe = pd.read_csv(file_path, sep=',') #, dtype='object'), header=None, names=np.arange(0, 20))
    #dataframe = dataframe.compute() # Lazy load
    dataframe.dropna(axis=1, how='all', inplace=True)
    dataframe.dropna(axis=0, how='all', inplace=True)
    file_name = file_path.split("/")[-1]
    dfs[file_name] = dataframe 

import os
from lxml import etree

xsd_directory = os.path.abspath("")+"/data"+"/NEMSIS_XSDs"  
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
                xsd_dict[value] = documentation.text

        xsd_dicts[xsd_filename] = xsd_dict
        print()
        print(xsd_filename)
        print(xsd_dict)

import pandas as pd
import os



dfs_hist = {}  

for file_name, df in dfs.items():

    matching_xsd_dict = None
    for xsd_name, xsd_dict in xsd_dicts.items():
        xsd_name_modified = xsd_name[1:].split('_')[0]
        if any(xsd_name_modified in col for col in df.columns.values):
            matching_xsd_dict = xsd_dict
            break

    if matching_xsd_dict:
        # Calculate the frequency of each response code using column number 2
        response_counts = df.iloc[:, -1].value_counts()

        response_counts.index = response_counts.index.map(lambda x: matching_xsd_dict.get((x), x))  # Use matching XSD dict

        # Store the result in the dictionary with the file name as the key
        dfs_hist[file_name] = response_counts

# Now, results contains a list of tuples where each tuple contains the file name and a DataFrame with ResponseCodes and Counts columns.

import matplotlib.pyplot as plt

for file_name, response_counts in dfs_hist.items():
    plt.figure(figsize=(10, 6))
    plt.bar(response_counts.index, response_counts.values)
    plt.xlabel("Response Code",fontsize=10)
    plt.ylabel("Count")
    plt.title(f"Histogram for {target_file_names[file_name]}")
    plt.xticks(rotation=45)  
    plt.savefig(f"figs/Histogram_plot_{target_file_names[file_name]}.png", bbox_inches="tight")
    plt.show()

