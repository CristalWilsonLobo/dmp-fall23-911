import matplotlib.pyplot as plt
import pandas as pd
from utility_methods import extract_specific_file_from_zip_archive

# Path to the ZIP file and the specific CSV file you want to extract
zip_file_path = 'data/processeddataCA.zip'
csv_file_name = 'processeddataCA/FACTPCRPROTOCOL_CA.csv'

# pull dataframe of specific file out of the zip archive
df = extract_specific_file_from_zip_archive(zip_file_path, csv_file_name)

# Now, df contains the data from the specific CSV file
print(df.head())

# Mapping of codes to descriptions
code_description2 = {
    7701001: 'Not Applicable',
    7701003: 'Not Recorded',
    3602001: 'Adult Only',
    3602003: 'General',
    3602005: 'Pediatric Only'
}

# Calculate the frequency of each response code
response_counts2 = df['eProtocol_02'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts2.index = response_counts2.index.map(code_description2)

# Mapping of codes to descriptions
code_description1 = {
    7701001: 'Not Applicable',
    7701003: 'Not Recorded',
    9914001: 'Airway',
    9914003: 'Airway-Failed',
    9914005: 'Airway-Obstruction/Foreign Body',
    9914007: 'Airway-Rapid Sequence Induction (RSI-Paralytic)',
    9914009: 'Airway-Sedation Assisted (Non-Paralytic)',
    9914011: 'Cardiac Arrest-Asystole',
    9914013: 'Cardiac Arrest-Hypothermia-Therapeutic',
    9914015: 'Cardiac Arrest-Pulseless Electrical Activity',
    9914017: 'Cardiac Arrest-Ventricular Fibrillation/ Pulseless Ventricular Tachycardia',
    9914019: 'Cardiac Arrest-Post Resuscitation Care',
    9914021: 'Environmental-Altitude Sickness',
    9914023: 'Environmental-Cold Exposure',
    9914025: 'Environmental-Frostbite/Cold Injury',
    9914027: 'Environmental-Heat Exposure/Exhaustion',
    9914029: 'Environmental-Heat Stroke/Hyperthermia',
    9914031: 'Environmental-Hypothermia',
    9914033: 'Exposure-Airway/Inhalation Irritants',
    9914035: 'Exposure-Biological/Infectious',
    9914037: 'Exposure-Blistering Agents',
    9914041: 'Exposure-Chemicals to Eye',
    9914043: 'Exposure-Cyanide',
    9914045: 'Exposure-Explosive/ Blast Injury',
    9914047: 'Exposure-Nerve Agents',
    9914049: 'Exposure-Radiologic Agents',
    9914051: 'General-Back Pain',
    9914053: 'General-Behavioral/Patient Restraint',
    9914055: 'General-Cardiac Arrest',
    9914057: 'General-Dental Problems',
    9914059: 'General-Epistaxis',
    9914061: 'General-Fever',
    9914063: 'General-Individualized Patient Protocol',
    9914065: 'General-Indwelling Medical Devices/Equipment',
    9914067: 'General-IV Access',
    9914069: 'General-Medical Device Malfunction',
    9914071: 'General-Pain Control',
    9914073: 'General-Spinal Immobilization/Clearance',
    9914075: 'General-Universal Patient Care/ Initial Patient Contact',
    9914077: 'Injury-Amputation',
    9914079: 'Injury-Bites and Envenomations-Land',
    9914081: 'Injury-Bites and Envenomations-Marine',
    9914083: 'Injury-Bleeding/ Hemorrhage Control',
    9914085: 'Injury-Burns-Thermal',
    9914087: 'Injury-Cardiac Arrest',
    9914089: 'Injury-Crush Syndrome',
    9914091: 'Injury-Diving Emergencies',
    9914093: 'Injury-Drowning/Near Drowning',
    9914095: 'Injury-Electrical Injuries',
    9914097: 'Injury-Extremity',
    9914099: 'Injury-Eye',
    9914101: 'Injury-Head',
    9914103: 'Injury-Impaled Object',
    9914105: 'Injury-Multisystem',
    9914107: 'Injury-Spinal Cord',
    9914109: 'Medical-Abdominal Pain',
    9914111: 'Medical-Allergic Reaction/Anaphylaxis',
    9914113: 'Medical-Altered Mental Status',
    9914115: 'Medical-Bradycardia',
    9914117: 'Medical-Cardiac Chest Pain',
    9914119: 'Medical-Diarrhea',
    9914121: 'Medical-Hyperglycemia',
    9914123: 'Medical-Hypertension',
    9914125: 'Medical-Hypoglycemia/Diabetic Emergency',
    9914127: 'Medical-Hypotension/Shock (Non-Trauma)',
    9914129: 'Medical-Influenza-Like Illness/ Upper Respiratory Infection',
    9914131: 'Medical-Nausea/Vomiting',
    9914133: 'Medical-Newborn/ Neonatal Resuscitation',
    9914135: 'General-Overdose/Poisoning/Toxic Ingestion',
    9914137: 'Medical-Pulmonary Edema/CHF',
    9914139: 'Medical-Respiratory Distress/Asthma/COPD/Reactive Airway',
    9914141: 'Medical-Seizure',
    9914143: 'Medical-ST-Elevation Myocardial Infarction (STEMI)',
    9914145: 'Medical-Stroke/TIA',
    9914147: 'Medical-Supraventricular Tachycardia (Including Atrial Fibrillation)',
    9914149: 'Medical-Syncope',
    9914151: 'Medical-Ventricular Tachycardia (With Pulse)',
    9914153: 'Not Done',
    9914155: 'OB/GYN-Childbirth/Labor/Delivery',
    9914157: 'OB/GYN-Eclampsia',
    9914159: 'OB/GYN-Gynecologic Emergencies',
    9914161: 'OB/GYN-Pregnancy Related Emergencies',
    9914163: 'OB/GYN-Post-partum Hemorrhage',
    9914165: 'Other',
    9914167: 'Exposure-Carbon Monoxide',
    9914169: 'Cardiac Arrest-Do Not Resuscitate',
    9914171: 'Cardiac Arrest-Special Resuscitation Orders',
    9914173: 'Exposure-Smoke Inhalation',
    9914175: 'General-Community Paramedicine / Mobile Integrated Healthcare',
    9914177: 'General-Exception Protocol',
    9914179: 'General-Extended Care Guidelines',
    9914181: 'General-Interfacility Transfers',
    9914183: 'General-Law Enforcement - Blood for Legal Purposes',
    9914185: 'General-Law Enforcement - Assist with Law Enforcement Activity',
    9914187: 'General-Neglect or Abuse Suspected',
    9914189: 'General-Refusal of Care',
    9914191: 'Injury-Mass/Multiple Casualties',
    9914193: 'Injury-Thoracic',
    9914195: 'Medical-Adrenal Insufficiency',
    9914197: 'Medical-Apparent Life Threatening Event (ALTE)',
    9914199: 'Medical-Tachycardia',
    9914201: 'Cardiac Arrest-Determination of Death / Withholding Resuscitative Efforts',
    9914203: 'Injury-Conducted Electrical Weapon (e.g., Taser)',
    9914205: 'Injury-Facial Trauma',
    9914207: 'Injury-General Trauma Management',
    9914209: 'Injury-Lightning/Lightning Strike',
    9914211: 'Injury-SCUBA Injury/Accidents',
    9914213: 'Injury-Topical Chemical Burn',
    9914215: 'Medical-Beta Blocker Poisoning/Overdose',
    9914217: 'Medical-Calcium Channel Blocker Poisoning/Overdose',
    9914219: 'Medical-Opioid Poisoning/Overdose',
    9914221: 'Medical-Respiratory Distress-Bronchiolitis',
    9914223: 'Medical-Respiratory Distress-Croup',
    9914225: 'Medical-Stimulant Poisoning/Overdos'
}

# Calculate the frequency of each response code
response_counts1 = df['eProtocol_01'].value_counts()

# Replace the code values with their descriptions for plotting
response_counts1.index = response_counts1.index.map(code_description1)

with pd.option_context('display.max_rows', None):
    print(response_counts1)

# Plotting
plt.figure(figsize=(15, 7))
response_counts2.plot(kind='bar', color='seagreen')
plt.title('Protocol Age Category')
plt.xlabel('Age Category of Protocol Used')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the entire figure with all subplots
filename = "figs/Protocol_Age_Category.png"
plt.savefig(filename)

plt.show()
