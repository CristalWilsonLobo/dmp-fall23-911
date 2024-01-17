import matplotlib.pyplot as plt

from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/ComputedElements_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

# Calculate the frequency of each response code
response_counts = df['Urbanicity'].value_counts()

# Plotting
plt.figure(figsize=(15, 7))
response_counts.plot(kind='bar', color='seagreen')
plt.title('Urbanicity Level')
plt.xlabel('Urbanicity Rating')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Urbanicity.png"
plt.savefig(filename)

plt.show()