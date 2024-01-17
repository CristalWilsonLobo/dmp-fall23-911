import matplotlib.pyplot as plt

from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/Pub_PCRevents_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

# Mapping of codes to descriptions
code_description = {
    7701001: 'Not Applicable',
    7701003: 'Not Recorded',
    3001001: 'No',
    3001003: 'Yes, Prior to Any EMS Arrival',
    3001005: 'Yes, After Any EMS Arrival'
}

# Calculate the frequency of each response code
response_counts = df['eArrest_01'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)

# Plotting
plt.figure(figsize=(15, 7))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Patient Experienced a Cardiac Arrest')
plt.xlabel('Cardiac Arrest Occurred')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Cardiac_Arrest1.png"
plt.savefig(filename)

# Mapping of codes to descriptions
code_description2 = {
    7701001: 'Not Applicable',
    7701003: 'Not Recorded',
    3002001: 'Cardiac (Presumed)',
    3002003: 'Drowning/Submersion',
    3002005: 'Drug Overdose',
    3002007: 'Electrocution',
    3002009: 'Exsanguination-Medical (Non-Traumatic)',
    3002011: 'Other',
    3002013: 'Respiratory/Asphyxia',
    3002015: 'Traumatic Cause',
}

# Calculate the frequency of each response code
response_counts2 = df['eArrest_02'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts2.index = response_counts2.index.map(code_description2)

# Plotting
plt.figure(figsize=(15, 7))
response_counts2.plot(kind='bar', color='seagreen')
plt.title('Cause of the Cardiac Arrest')
plt.xlabel('Etiology of the Cardiac Arrest')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Cardiac_Arrest2.png"
plt.savefig(filename)

plt.show()
