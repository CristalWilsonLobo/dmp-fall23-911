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
    9906001: 'Female',
    9906003: 'Male',
    9906007: 'Female-to-Male, Transgender Male',
    9906009: 'Male-to-Female, Transgender Female',
    9906011: 'Other, neither exclusively male or female',
    9906005: 'Unknown (Unable to Determine)'
}

# Calculate the frequency of each response code
response_counts = df['ePatient_13'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)

# Plotting
plt.figure(figsize=(15, 7))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Patient Gender')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Patient_Gender.png"
plt.savefig(filename)

plt.show()
