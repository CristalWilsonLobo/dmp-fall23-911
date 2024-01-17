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
    4219001: 'Critical (Red)',
    4219003: 'Emergent (Yellow)',
    4219005: 'Lower Acuity (Green)',
    4219007: 'Dead without Resuscitation Efforts (Black)',
    4219009: 'Dead with Resuscitation Efforts (Black)',
    4219011: 'Non-Acute/Routine'
}

# Calculate the frequency of each response code
response_counts = df['eDisposition_19'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)

# Plotting
plt.figure(figsize=(15, 7))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Acuity of Patients Condition After EMS Care ')
plt.xlabel('Acuity')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Patient_Acuity.png"
plt.savefig(filename)

# Mapping of codes to descriptions
code_description = {
    7701001: 'Not Applicable',
    7701003: 'Not Recorded',
    2708001: 'Red - Immediate',
    2708003: 'Yellow - Delayed',
    2708005: 'Green - Minimal (Minor)',
    2708007: 'Gray - Expectant',
    2708009: 'Black - Deceased'
}

# Calculate the frequency of each response code
response_counts = df['eScene_08'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)

# Plotting
plt.figure(figsize=(15, 7))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Triage Classification for MCI Patient')
plt.xlabel('Triage Classification')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Patient_Triage.png"
plt.savefig(filename)

plt.show()
