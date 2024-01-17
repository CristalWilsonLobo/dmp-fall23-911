import matplotlib.pyplot as plt

from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/FACTPCRTRANSPORTDELAY_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

# Mapping of codes to descriptions
code_description = {
    7701001: 'Not Applicable',
    7701003: 'Not Recorded',
    2211001: 'Crowd',
    2211003: 'Directions/Unable to Locate',
    2211005: 'Distance',
    2211007: 'Diversion',
    2211009: 'HazMat',
    2211011: 'None/No Delay',
    2211013: 'Other',
    2211015: 'Rendezvous Transport Unavailable',
    2211017: 'Route Obstruction (e.g., Train)',
    2211019: 'Safety',
    2211021: 'Staff Delay',
    2211023: 'Traffic',
    2211025: 'Vehicle Crash Involving this Unit',
    2211027: 'Vehicle Failure of this Unit',
    2211029: 'Weather',
    2211031: 'Patient Condition Change (e.g., Unit Stopped)'
}

# Calculate the frequency of each response code
response_counts = df['eResponse_11'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)

# Plotting
plt.figure(figsize=(15, 7))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Type of Transport Delay')
plt.xlabel('Transport Delay')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Type_Transport_Delay.png"
plt.savefig(filename)

plt.show()
