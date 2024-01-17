import matplotlib.pyplot as plt

from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/FACTPCRSCENEDELAY_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

# Mapping of codes to descriptions
code_description = {
    7701001: 'Not Applicable',
    7701003: 'Not Recorded',
    2210001: 'Awaiting Air Unit',
    2210003: 'Awaiting Ground Unit',
    2210005: 'Crowd',
    2210007: 'Directions/Unable to Locate',
    2210009: 'Distance',
    2210011: 'Extrication',
    2210013: 'HazMat',
    2210015: 'Language Barrier',
    2210017: 'None/No Delay',
    2210019: 'Other',
    2210021: 'Patient Access',
    2210023: 'Safety-Crew/Staging',
    2210025: 'Safety-Patient',
    2210027: 'Staff Delay',
    2210029: 'Traffic',
    2210031: 'Triage/Multiple Patients',
    2210033: 'Vehicle Crash Involving this Unit',
    2210035: 'Vehicle Failure of this Unit',
    2210037: 'Weather',
    2210039: 'Mechanical Issue-Unit, Equipment, etc.'
}

# Calculate the frequency of each response code
response_counts = df['eResponse_10'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)

# Plotting
plt.figure(figsize=(15, 7))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Type of Scene Delay')
plt.xlabel('Scene Delay')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Type_Scene_Delay.png"
plt.savefig(filename)

plt.show()
