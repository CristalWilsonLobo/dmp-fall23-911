import matplotlib.pyplot as plt

from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/FACTPCRWORKRELATEDEXPOSURE_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

# Mapping of codes to descriptions
code_description = {
    9923001: 'No',
    9923003: 'Yes',
    7701001: 'Not Applicable',
    7701003: 'Not Recorded'
}

# Calculate the frequency of each response code
response_counts = df['eOther_05'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)

# Plotting
plt.figure(figsize=(15, 7))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Patient Race')
plt.xlabel('Race')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/EMS_worker_injury.png"
plt.savefig(filename)

plt.show()
