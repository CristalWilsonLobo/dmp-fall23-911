import matplotlib.pyplot as plt

from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/FACTPCRTURNAROUNDDELAY_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

# Mapping of codes to descriptions
code_description = {
    2212001: 'Clean-up',
    2212003: 'Decontamination',
    2212005: 'Distance',
    2212007: 'Documentation',
    2212009: 'ED Overcrowding / Transfer of Care',
    2212011: 'Equipment Failure',
    2212013: 'Equipment/Supply Replenishment',
    2212015: 'None/No Delay',
    2212017: 'Other',
    2212019: 'Rendezvous Transport Unavailable',
    2212021: 'Route Obstruction (e.g., Train)',
    2212023: 'Staff Delay',
    2212025: 'Traffic',
    2212027: 'Vehicle Crash of this Unit',
    2212029: 'Vehicle Failure of this Unit',
    2212031: 'Weather',
    2212033: 'EMS Crew Accompanies Patient for Facility Procedure',
    7701001: 'Not Applicable',
    7701003: 'Not Recorded'
}

# Calculate the frequency of each response code
response_counts = df['eResponse_12'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)
response_countsNoNA = response_counts

# Plotting
plt.figure(figsize=(15, 7))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Type of Turn Around Delay')
plt.xlabel('Type of Turn Around Delay')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Type_Turnaround_Delay.png"
plt.savefig(filename)

plt.show()

""" noNAs = response_counts.drop('Not Applicable').drop('Not Recorded').drop('None/No Delay')
print(noNAs)
noNAs.plot(kind='bar', color='seagreen')
plt.show() """
