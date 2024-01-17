import matplotlib.pyplot as plt

from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/FACTPCRARRESTRESUSCITATION_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

# Mapping of codes to descriptions
code_description = {
    7701001: 'Not Applicable',
    7701003: 'Not Recorded',
3003001: 'Attempted Defibrillation',
3003003: 'Attempted Ventilation',
3003005: 'Initiated Chest Compressions',
3003007: 'Not Attempted-Considered Futile',
3003009: 'Not Attempted-DNR Orders',
3003011: 'Not Attempted-Signs of Circulation'
}

# Calculate the frequency of each response code
response_counts = df['eArrest_03'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)

# Plotting
plt.figure(figsize=(10, 10))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Resuscitation Attempted By EMS')
plt.xlabel('Response Type')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Resuscitation_Attempted.png"
plt.savefig(filename)

plt.show()
