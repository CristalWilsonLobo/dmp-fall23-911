import matplotlib.pyplot as plt

from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/FACTPCRTRAUMACRITERIA_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

# Mapping of codes to descriptions
code_description = {
    7701001: 'Not Applicable',
    7701003: 'Not Recorded',
    2903001: 'Amputation proximal to wrist or ankle',
    2903003: 'Crushed, degloved, mangled, or pulseless extremity',
    2903005: 'Chest wall instability, deformity, or suspected flail chest',
    2903007: 'Glasgow Coma Score <= 13 (DEPRECATED)',
    2903009: 'Skull deformity, suspected skull fracture',
    2903011: 'Paralysis (DEPRECATED)',
    2903013: 'Suspected pelvic fracture',
    2903015: 'Penetrating injuries to head, neck, torso, and proximal extremities',
    2903017: 'Concerning Respiratory Rate (DEPRECATED)',
    2903019: 'Systolic Blood Pressure <90 mmHg (DEPRECATED)',
    2903021: 'Suspected fracture of two or more proximal long bones',
    2903023: 'Active bleeding requiring a tourniquet or wound packing with continuous pressure',
    2903025: 'Age >= 10 years: HR > SBP',
    2903027: 'Age >= 65 years: SBP < 110 mmHg',
    2903029: 'Age 0-9 years: SBP < 70mm Hg + (2 x age in years)',
    2903031: 'Age 10-64 years: SBP < 90 mmHg',
    2903033: 'Respiratory distress or need for respiratory support',
    2903035: 'Room-air pulse oximetry < 90%',
    2903037: 'RR < 10 or > 29 breaths/min',
    2903039: 'Suspected spinal injury with new motor or sensory loss',
    2903041: 'Unable to follow commands (motor GCS < 6)'
}

# Calculate the frequency of each response code
response_counts = df['eInjury_03'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)

# Plotting
plt.figure(figsize=(10, 10))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Trauma Triage Criteria (High Risk Factors for Serious Injury) ')
plt.xlabel('Risk Factor Type')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/High_Risk_Factors.png"
plt.savefig(filename)

plt.show()
