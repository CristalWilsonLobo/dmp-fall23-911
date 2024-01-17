import matplotlib.pyplot as plt

from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/FACTPCRVITAL_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

df1 = df[df.eVitals_10 < 1000]

# Plotting
plt.figure(figsize=(15, 7))
plt.hist(df1['eVitals_10'],bins=100)
plt.xlim((1,300))
plt.title('Patients Heart Rate')
plt.xlabel('Heart Rate in Beats Per Minute')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Heart_Rate.png"
plt.savefig(filename)

df2 = df[df.eVitals_06 < 1000]

# Plotting
plt.figure(figsize=(15, 7))
plt.hist(df2['eVitals_06'],bins=100)
plt.xlim((1,300))
plt.title('Patients Systolic Blood Pressure')
plt.xlabel('Systolic Blood Pressure in mmHg')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Blood_Pressure.png"
plt.savefig(filename)

plt.show()
