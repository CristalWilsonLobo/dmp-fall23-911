import matplotlib.pyplot as plt

from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/FACTPCRDISPATCHDELAY_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

# Mapping of codes to descriptions
code_description = {
    2208001: 'Caller (Uncooperative)',
    2208003: 'Diversion/Failure (of previous unit)',
    2208005: 'High Call Volume',
    2208007: 'Language Barrier',
    2208009: 'Incomplete Address Information Provided',
    2208011: 'No EMS Vehicles (Units) Available',
    2208013: 'None/No Delay',
    2208015: 'Other',
    2208017: 'Technical Failure (Computer, Phone etc.)',
    2208019: 'Communication Specialist-Assignment Error',
    2208021: 'No Receiving MD, Bed, H',
    7701001: 'Not Applicable',
    7701003: 'Not Recorded'
}


# Calculate the frequency of each response code
response_counts = df['eResponse_08'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts.index = response_counts.index.map(code_description)

# Plotting all counts
plt.figure(figsize=(15, 7))
ax_all = response_counts.plot(kind='bar', color='lightblue')
plt.title('All Types of Dispatch Delay')
plt.xlabel('Dispatch Delay')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Annotating the bar plot with the actual counts
for p in ax_all.patches:
    ax_all.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

filename_all = "figs/All_Types_Dispatch_Delay.png"
plt.savefig(filename_all)

plt.show()

# Exclude the specific columns for the main_counts
excluded_labels = ['None/No Delay', 'Not Recorded', 'Other', 'Not Applicable']
main_counts = response_counts.drop(excluded_labels)

# Plotting the main_counts
plt.figure(figsize=(15, 7))
ax_main = main_counts.plot(kind='bar', color='seagreen')
plt.title('Main Types of Dispatch Delay (Excluding missing Labels and No Delay)')
plt.xlabel('Dispatch Delay')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Annotating the bar plot with the actual counts
for p in ax_main.patches:
    ax_main.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

filename_main = "figs/Main_Types_Dispatch_Delay_Excluding_Specific.png"
plt.savefig(filename_main)

plt.show()
