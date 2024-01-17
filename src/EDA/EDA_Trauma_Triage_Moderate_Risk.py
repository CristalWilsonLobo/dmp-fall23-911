import matplotlib.pyplot as plt

from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/FACTPCRINJURYRISKFACTOR_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

# Mapping of codes to descriptions
code_description = {
    7701001: 'Not Applicable',
    7701003: 'Not Recorded',
    2904001: 'Pedestrian/bicycle rider thrown, run over, or with significant impact',
    2904003: 'Fall Adults: > 20 ft. (one story is equal to 10 ft.) (DEPRECATED)',
    2904005: 'Fall Children: > 10 ft. or 2-3 times the height of the child (DEPRECATED)',
    2904007: 'Auto Crash: Death in passenger compartment',
    2904009: 'Auto Crash: Partial or complete ejection',
    2904011: 'Auto Crash: Significant intrusion (including roof): need for extrication',
    2904013: 'Auto Crash: Vehicle telemetry data consistent with severe injury',
    2904015: 'Motorcycle Crash > 20 MPH (DEPRECATED)',
    2904017: 'SBP < 110 for age > 65 (DEPRECATED)',
    2904019: 'Anticoagulant use',
    2904021: 'Pregnancy > 20 weeks',
    2904023: 'Other EMS judgment',
    2904025: 'Burn, without other trauma (DEPRECATED)',
    2904027: 'Burns in conjunction with trauma',
    2904029: 'Auto Crash: Child (age 0-9 years) unrestrained or in unsecured child safety seat',
    2904031: 'Fall from height > 10 feet (all ages)',
    2904033: 'Low-level falls in young children or older adults with significant head impact',
    2904035: 'Rider separated from transport vehicle with significant impact (eg, motorcycle, ATV, horse, etc.)',
    2904037: 'Special, high-resource healthcare needs',
    2904039: 'Suspicion of child abuse'
}

# Calculate the frequency of each response code
response_counts = df['eInjury_04'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)

# Plotting
plt.figure(figsize=(10, 10))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Trauma Triage Criteria (Medium Risk Factors for Serious Injury) ')
plt.xlabel('Risk Factor Type')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Moderate_Risk_Factors.png"
plt.savefig(filename)

plt.show()
