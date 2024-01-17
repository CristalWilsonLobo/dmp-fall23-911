import pandas as pd
import numpy as np
import os
from lxml import etree
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile

def unzip_to_folder(zip_file_path, target_folder):
    # Check if the folder where we want to unzip the files already exists
    if not os.path.exists(target_folder):
        # Folder does not exist, so we can proceed to unzip the file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(target_folder)
            print(f"Unzipped the file to {target_folder}")
    else:
        # Folder already exists, implying the file has already been unzipped
        print(f"The folder {target_folder} already exists. No need to unzip.")



# Merge primary files "Pub_PCRevents_CA.csv" and "ComputedElements_CA.csv"
def extract_primary_data():

    computedElements_file_path = os.path.abspath("")+"/data/processeddataCA/ComputedElements_CA.csv"
    Pub_PCRevents_file_path = os.path.abspath("")+"/data/processeddataCA/Pub_PCRevents_CA.csv"

    computedElements_dataframe = pd.read_csv(computedElements_file_path, sep=',',  index_col=0, low_memory=False) 
    computedElements_dataframe.dropna(axis=1, how='all', inplace=True)
    print(computedElements_dataframe.head)
    print(computedElements_dataframe.shape)

    pub_PCRevents_dataframe = pd.read_csv(Pub_PCRevents_file_path, sep=',', index_col=0, low_memory=False) 
    pub_PCRevents_dataframe.dropna(axis=1, how='all', inplace=True)
    print(pub_PCRevents_dataframe.head)
    print(pub_PCRevents_dataframe.shape)

    return computedElements_dataframe,pub_PCRevents_dataframe

def combinePrimaryDfs(computedElements_dataframe,pub_PCRevents_dataframe):
    merged_dataframe = computedElements_dataframe.merge(pub_PCRevents_dataframe, on='PcrKey')
    print(merged_dataframe.head())
    print(merged_dataframe.shape)
    return merged_dataframe

def dataframe_stats(df):
    print(df.head)
    print(df.shape)
    df.dropna(axis=1, how='all', inplace=True)

# To read all the files in the processeddataCA folder that have "PCR" keyword in the file name and storing them in a dataframe which are in turn stored in a dictionary that holds all dataframes for each file
# Extracting only PCR related files as we have already extracted ComputedElements_CA and Pub_PCRevents_CA as our primary files, hence used the file pattern as "PCR" to exclude these two files

def extract_data():
    
    directory_path = os.path.abspath("") + "/data/processeddataCA/"
    file_paths = glob.glob(os.path.join(directory_path, "*.csv"))
    dataframes_dict = {}
    excluded_files = ["Pub_PCRevents_CA.csv", "ComputedElements_CA.csv"]

    for file_path in file_paths:
        file_name = os.path.basename(file_path)

        if file_name not in excluded_files:
            print("Storing file", file_name, "in a dataframe")
            df = pd.read_csv(file_path, sep=',', index_col=0, low_memory=False)
            dataframes_dict[file_name] = df
    print("")
    print("The dictionary now holds a list of all files in a dataframe")

    for key, value in dataframes_dict.items():
        print(f"\nFile: {key}")
        print(value.head())

    return dataframes_dict


# To merge all the files in processeddataCA folder stored in above dataframes_dict to our primary dataframe consisting of files ComputedElements_CA and Pub_PCRevents_CA
# Steps : 
# Merging takes place on common column match viz PcrKey
# 
def combineDfs(df_main,df_dict):
    print("Looping through each file in the dataframe dictionary and merging with main dataframe")
    for df_name, df in df_dict.items():
        merged_df = pd.merge(df_main, df, on="PcrKey", how="inner", suffixes=('', '_y'))
        for column in df.columns:
            if "PcrKey" not in column and column not in df_main.columns:
                print("Column ",column,"is not present in main dataframe, hence adding it")
                df_main[column] = merged_df[column]
            elif "PcrKey" not in column:
                print("Column ",column,"is present in main dataframe, checking if all values match with the main dataframe's column")
                column_x = column
                column_y = f"{column}_y"
                merged_df.reset_index(drop=True,inplace=True)
                #merged_df = merged_df.apply(pd.to_numeric, errors='coerce')
                if merged_df[column_x].dtypes == merged_df[column_y].dtypes:
                    #are_equal = ((merged_df[column_x]) == (merged_df[column_y])).all() 
                    are_equal = merged_df[column_x].equals(merged_df[column_y])
                    #match = (merged_df[column_x].apply(pd.to_numeric, errors='coerce')) == (merged_df[column_y].apply(pd.to_numeric, errors='coerce')) 
                #else:
                 #   match = (merged_df[column_x].astype(str) == merged_df[column_y].astype(str))
                    if not are_equal:
                        print("Column ",column,"values does not match with the main dataframe's column, hence adding it to the main dataframe")
                        df_main[column_y] = merged_df[column_y]


    return df_main            
                
    

def load_XSD_Dictionary():

    xsd_directory = os.path.abspath("") + "/data/NEMSIS_XSDs"
    xsd_dicts = {}

    for xsd_filename in os.listdir(xsd_directory):
        if xsd_filename.endswith(".xsd"):
            xsd_path = os.path.join(xsd_directory, xsd_filename)
            xsd_dict = {}
            tree = etree.parse(xsd_path)
            root = tree.getroot()

            for enumeration in root.xpath("//xs:enumeration", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}):
                value = enumeration.get("value")
                documentation = enumeration.find(".//xs:documentation", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"})
                
                if value is not None and documentation is not None:
                    #xsd_dict[value] = documentation.text
                    try:
                        #key = np.int64(value)
                        key =  str(value).replace(" ", "")
                        xsd_dict[key] = documentation.text
                    except ValueError:
                        # Handle the case where 'value' is not a valid int64
                        xsd_dict[str(value).replace(" ", "")] = documentation.text
                    
            xsd_dict['7701001'] = 'Not Applicable'
            xsd_dict['7701003'] = 'Not Recorded'

            if 'eArrest' in xsd_filename:
                xsd_dict['3011001'] = 'Asystole'
                xsd_dict['3011005'] = 'PEA'
                xsd_dict['3011007'] = 'Unknown AED Non-Shockable Rhythm'
                xsd_dict['3011009'] = 'Unknown AED Shockable Rhythm'
                xsd_dict['3011011'] = 'Ventricular Fibrillation'
                xsd_dict['3011013'] = 'Ventricular Tachycardia-Pulseless'

            if 'ePatient' in xsd_filename:
                xsd_dict['9906001'] = 'Female'
                xsd_dict['9906003'] = 'Male'
                xsd_dict['9906007'] = 'Female-to-Male, Transgender Male'
                xsd_dict['9906009'] = 'Male-to-Female, Transgender Female'
                xsd_dict['9906011'] = 'Other, neither exclusively male or female'
                xsd_dict['9906005'] = 'Unknown (Unable to Determine)'

            if 'eResponse' in xsd_filename:
                xsd_dict['2207011'] = 'Air Transport-Helicopter'
                xsd_dict['2207013'] = 'Air Transport-Fixed Wing'
                xsd_dict['2207015'] = 'Ground Transport (ALS Equipped)'
                xsd_dict['2207017'] = 'Ground Transport (BLS Equipped)'
                xsd_dict['2207019'] = 'Ground Transport (Critical Care Equipped)'
                xsd_dict['2207021'] = 'Non-Transport-Medical Treatment (ALS Equipped)'
                xsd_dict['2207023'] = 'Non-Transport-Medical Treatment (BLS Equipped)'
                xsd_dict['2207025'] = 'Wheel Chair Van/Ambulette'
                xsd_dict['2207027'] = 'Non-Transport-No Medical Equipment'

            if 'eScene01' in xsd_filename:
                xsd_dict['9923001'] = 'No'
                xsd_dict['9923003'] = 'Yes'

            if 'eScene07' in xsd_filename:
                xsd_dict['9923001'] = 'No'
                xsd_dict['9923003'] = 'Yes'

            if 'eSituation02' in xsd_filename:
                xsd_dict['9922001'] = 'No'
                xsd_dict['9922003'] = 'Unknown'
                xsd_dict['9922005'] = 'Yes'
             
            if 'eDisposition23' in xsd_filename:
                xsd_dict['9908001'] = 'Behavioral Health'
                xsd_dict['9908003'] = 'Burn Center'
                xsd_dict['9908005'] = 'Critical Access Hospital'
                xsd_dict['9908007'] = 'Hospital (General)'
                xsd_dict['9908009'] = 'Neonatal Center'
                xsd_dict['9908011'] = 'Pediatric Center'
                xsd_dict['9908019'] = 'Rehab Center'
                xsd_dict['9908021'] = 'Trauma Center Level 1'
                xsd_dict['9908023'] = 'Trauma Center Level 2'
                xsd_dict['9908025'] = 'Trauma Center Level 3'
                xsd_dict['9908027'] = 'Trauma Center Level 4'
                xsd_dict['9908029'] = 'Trauma Center Level 5'
                xsd_dict['9908031'] = 'Cardiac-STEMI/PCI Capable'
                xsd_dict['9908033'] = 'Cardiac-STEMI/PCI Capable (24/7)'
                xsd_dict['9908035'] = 'Cardiac-STEMI/Non-PCI Capable'
                xsd_dict['9908037'] = 'Stroke-Acute Stroke Ready Hospital (ASRH)'
                xsd_dict['9908039'] = 'Stroke-Primary Stroke Center (PSC)'
                xsd_dict['9908041'] = 'Stroke-Thrombectomy-Capable Stroke Center (TSC)'
                xsd_dict['9908043'] = 'Stroke-Comprehensive Stroke Center (CSC)'
                xsd_dict['9908045'] = 'Cancer Center'
                xsd_dict['9908047'] = 'Labor and Delivery'


            if 'eProtocol01' in xsd_filename:
                xsd_dict['9914001'] = 'Airway'
                xsd_dict['9914003'] = 'Airway-Failed'
                xsd_dict['9914005'] = 'Airway-Obstruction/Foreign Body'
                xsd_dict['9914007'] = 'Airway-Rapid Sequence Induction (RSI-Paralytic)'
                xsd_dict['9914009'] = 'Airway-Sedation Assisted (Non-Paralytic)'
                xsd_dict['9914011'] = 'Cardiac Arrest-Asystole'
                xsd_dict['9914013'] = 'Cardiac Arrest-Hypothermia-Therapeutic'
                xsd_dict['9914015'] = 'Cardiac Arrest-Pulseless Electrical Activity'
                xsd_dict['9914017'] = 'Cardiac Arrest-Ventricular Fibrillation/ Pulseless Ventricular Tachycardia'
                xsd_dict['9914019'] = 'Cardiac Arrest-Post Resuscitation Care'
                xsd_dict['9914021'] = 'Environmental-Altitude Sickness'
                xsd_dict['9914023'] = 'Environmental-Cold Exposure'
                xsd_dict['9914025'] = 'Environmental-Frostbite/Cold Injury'
                xsd_dict['9914027'] = 'Environmental-Heat Exposure/Exhaustion'
                xsd_dict['9914029'] = 'Environmental-Heat Stroke/Hyperthermia'
                xsd_dict['9914031'] = 'Environmental-Hypothermia'
                xsd_dict['9914033'] = 'Exposure-Airway/Inhalation Irritants'
                xsd_dict['9914035'] = 'Exposure-Biological/Infectious'
                xsd_dict['9914037'] = 'Exposure-Blistering Agents'
                xsd_dict['9914041'] = 'Exposure-Chemicals to Eye'
                xsd_dict['9914043'] = 'Exposure-Cyanide'
                xsd_dict['9914045'] = 'Exposure-Explosive/ Blast Injury'
                xsd_dict['9914047'] = 'Exposure-Nerve Agents'
                xsd_dict['9914049'] = 'Exposure-Radiologic Agents'
                xsd_dict['9914051'] = 'General-Back Pain'
                xsd_dict['9914053'] = 'General-Behavioral/Patient Restraint'
                xsd_dict['9914055'] = 'General-Cardiac Arrest'
                xsd_dict['9914057'] = 'General-Dental Problems'
                xsd_dict['9914059'] = 'General-Epistaxis'
                xsd_dict['9914061'] = 'General-Fever'
                xsd_dict['9914063'] = 'General-Individualized Patient Protocol'
                xsd_dict['9914065'] = 'General-Indwelling Medical Devices/Equipment'
                xsd_dict['9914067'] = 'General-IV Access'
                xsd_dict['9914069'] = 'General-Medical Device Malfunction'
                xsd_dict['9914071'] = 'General-Pain Control'
                xsd_dict['9914073'] = 'General-Spinal Immobilization/Clearance'
                xsd_dict['9914075'] = 'General-Universal Patient Care/ Initial Patient Contact'
                xsd_dict['9914077'] = 'Injury-Amputation'
                xsd_dict['9914079'] = 'Injury-Bites and Envenomations-Land'
                xsd_dict['9914081'] = 'Injury-Bites and Envenomations-Marine'
                xsd_dict['9914083'] = 'Injury-Bleeding/ Hemorrhage Control'
                xsd_dict['9914085'] = 'Injury-Burns-Thermal'
                xsd_dict['9914087'] = 'Injury-Cardiac Arrest'
                xsd_dict['9914089'] = 'Injury-Crush Syndrome'
                xsd_dict['9914091'] = 'Injury-Diving Emergencies'
                xsd_dict['9914093'] = 'Injury-Drowning/Near Drowning'
                xsd_dict['9914095'] = 'Injury-Electrical Injuries'
                xsd_dict['9914097'] = 'Injury-Extremity'
                xsd_dict['9914099'] = 'Injury-Eye'
                xsd_dict['9914101'] = 'Injury-Head'
                xsd_dict['9914103'] = 'Injury-Impaled Object'
                xsd_dict['9914105'] = 'Injury-Multisystem'
                xsd_dict['9914107'] = 'Injury-Spinal Cord'
                xsd_dict['9914109'] = 'Medical-Abdominal Pain'
                xsd_dict['9914111'] = 'Medical-Allergic Reaction/Anaphylaxis'
                xsd_dict['9914113'] = 'Medical-Altered Mental Status'
                xsd_dict['9914115'] = 'Medical-Bradycardia'
                xsd_dict['9914117'] = 'Medical-Cardiac Chest Pain'
                xsd_dict['9914119'] = 'Medical-Diarrhea'
                xsd_dict['9914121'] = 'Medical-Hyperglycemia'
                xsd_dict['9914123'] = 'Medical-Hypertension'
                xsd_dict['9914125'] = 'Medical-Hypoglycemia/Diabetic Emergency'
                xsd_dict['9914127'] = 'Medical-Hypotension/Shock (Non-Trauma)'
                xsd_dict['9914129'] = 'Medical-Influenza-Like Illness/ Upper Respiratory Infection'
                xsd_dict['9914131'] = 'Medical-Nausea/Vomiting'
                xsd_dict['9914133'] = 'Medical-Newborn/ Neonatal Resuscitation'
                xsd_dict['9914135'] = 'General-Overdose/Poisoning/Toxic Ingestion'
                xsd_dict['9914137'] = 'Medical-Pulmonary Edema/CHF'
                xsd_dict['9914139'] = 'Medical-Respiratory Distress/Asthma/COPD/Reactive Airway'
                xsd_dict['9914141'] = 'Medical-Seizure'
                xsd_dict['9914143'] = 'Medical-ST-Elevation Myocardial Infarction (STEMI)'
                xsd_dict['9914145'] = 'Medical-Stroke/TIA'
                xsd_dict['9914147'] = 'Medical-Supraventricular Tachycardia (Including Atrial Fibrillation)'
                xsd_dict['9914149'] = 'Medical-Syncope'
                xsd_dict['9914151'] = 'Medical-Ventricular Tachycardia (With Pulse)'
                xsd_dict['9914153'] = 'Not Done'
                xsd_dict['9914155'] = 'OB/GYN-Childbirth/Labor/Delivery'
                xsd_dict['9914157'] = 'OB/GYN-Eclampsia'
                xsd_dict['9914159'] = 'OB/GYN-Gynecologic Emergencies'
                xsd_dict['9914161'] = 'OB/GYN-Pregnancy Related Emergencies'
                xsd_dict['9914163'] = 'OB/GYN-Post-partum Hemorrhage'
                xsd_dict['9914165'] = 'Other'
                xsd_dict['9914167'] = 'Exposure-Carbon Monoxide'
                xsd_dict['9914169'] = 'Cardiac Arrest-Do Not Resuscitate'
                xsd_dict['9914171'] = 'Cardiac Arrest-Special Resuscitation Orders'
                xsd_dict['9914173'] = 'Exposure-Smoke Inhalation'
                xsd_dict['9914175'] = 'General-Community Paramedicine / Mobile Integrated Healthcare'
                xsd_dict['9914177'] = 'General-Exception Protocol'
                xsd_dict['9914179'] = 'General-Extended Care Guidelines'
                xsd_dict['9914181'] = 'General-Interfacility Transfers'
                xsd_dict['9914183'] = 'General-Law Enforcement - Blood for Legal Purposes'
                xsd_dict['9914185'] = 'General-Law Enforcement - Assist with Law Enforcement Activity'
                xsd_dict['9914187'] = 'General-Neglect or Abuse Suspected'
                xsd_dict['9914189'] = 'General-Refusal of Care'
                xsd_dict['9914191'] = 'Injury-Mass/Multiple Casualties'
                xsd_dict['9914193'] = 'Injury-Thoracic'
                xsd_dict['9914195'] = 'Medical-Adrenal Insufficiency'
                xsd_dict['9914197'] = 'Medical-Apparent Life Threatening Event (ALTE)'
                xsd_dict['9914199'] = 'Medical-Tachycardia'
                xsd_dict['9914201'] = 'Cardiac Arrest-Determination of Death / Withholding Resuscitative Efforts'
                xsd_dict['9914203'] = 'Injury-Conducted Electrical Weapon (e.g., Taser)'
                xsd_dict['9914205'] = 'Injury-Facial Trauma'
                xsd_dict['9914207'] = 'Injury-General Trauma Management'
                xsd_dict['9914209'] = 'Injury-Lightning/Lightning Strike'
                xsd_dict['9914211'] = 'Injury-SCUBA Injury/Accidents'
                xsd_dict['9914213'] = 'Injury-Topical Chemical Burn'
                xsd_dict['9914215'] = 'Medical-Beta Blocker Poisoning/Overdose'
                xsd_dict['9914217'] = 'Medical-Calcium Channel Blocker Poisoning/Overdose'
                xsd_dict['9914219'] = 'Medical-Opioid Poisoning/Overdose'
                xsd_dict['9914221'] = 'Medical-Respiratory Distress-Bronchiolitis'
                xsd_dict['9914223'] = 'Medical-Respiratory Distress-Croup'
                xsd_dict['9914225'] = 'Medical-Stimulant Poisoning/Overdose'

            if 'eProtocol02' in xsd_filename:
                xsd_dict['3602001'] = 'Adult Only'
                xsd_dict['3602003'] = 'General'
                xsd_dict['3602005'] = 'Pediatric Only'

            if 'eMedications03' in xsd_filename:
                xsd_dict['8801001'] = 'Contraindication Noted'
                xsd_dict['8801003'] = 'Denied By Order'
                xsd_dict['8801007'] = 'Medication Allergy'
                xsd_dict['8801009'] = 'Medication Already Taken'
                xsd_dict['8801019'] = 'Refused'
                xsd_dict['8801023'] = 'Unable to Complete'
                xsd_dict['8801027'] = 'Order Criteria Not Met'
                xsd_dict['9924003'] = 'RxNorm'
                xsd_dict['9924005'] = 'SNOMED-CT'

            if 'eMedications07' in xsd_filename:
                xsd_dict['9916001'] = 'Improved'
                xsd_dict['9916003'] = 'Unchanged'
                xsd_dict['9916005'] = 'Worse'

            if 'eMedications10' in xsd_filename:
                xsd_dict['9905001'] = 'Advanced Emergency Medical Technician (AEMT)'
                xsd_dict['9905002'] = 'Emergency Medical Technician - Intermediate'
                xsd_dict['9905003'] = 'Emergency Medical Responder (EMR)'
                xsd_dict['9905005'] = 'Emergency Medical Technician (EMT)'
                xsd_dict['9905007'] = 'Paramedic'
                xsd_dict['9905019'] = 'Other Healthcare Professional'
                xsd_dict['9905021'] = 'Other Non-Healthcare Professional'
                xsd_dict['9905025'] = 'Physician'
                xsd_dict['9905027'] = 'Respiratory Therapist'
                xsd_dict['9905029'] = 'Student'
                xsd_dict['9905031'] = 'Critical Care Paramedic'
                xsd_dict['9905033'] = 'Community Paramedicine'
                xsd_dict['9905035'] = 'Nurse Practitioner'
                xsd_dict['9905037'] = 'Physician Assistant'
                xsd_dict['9905039'] = 'Licensed Practical Nurse (LPN)'
                xsd_dict['9905041'] = 'Registered Nurse'
                xsd_dict['9905043'] = 'Patient'
                xsd_dict['9905045'] = 'Lay Person'
                xsd_dict['9905047'] = 'Law Enforcement'
                xsd_dict['9905049'] = 'Family Member'
                xsd_dict['9905051'] = 'Fire Personnel (non EMS)'

            if 'eMedications02' in xsd_filename:
                xsd_dict['9923001'] = 'No'
                xsd_dict['9923003'] = 'Yes'

            if 'eOther05' in xsd_filename:
                xsd_dict['9923001'] = 'No'
                xsd_dict['9923003'] = 'Yes'

            if 'ePatient14' in xsd_filename:
                xsd_dict['2514001'] = 'American Indian or Alaska Native'
                xsd_dict['2514003'] = 'Asian'
                xsd_dict['2514005'] = 'Black or African American'
                xsd_dict['2514007'] = 'Hispanic or Latino'
                xsd_dict['2514009'] = 'Native Hawaiian or Other Pacific Islander'
                xsd_dict['2514011'] = 'White'


            xsd_dicts[xsd_filename] = xsd_dict
            print("List of values for variable : ",xsd_filename)
            print(xsd_dict)
            print()
    return xsd_dicts

def updateCodes(merged_dataframe,xsd_dicts):
    for col in merged_dataframe.columns.values:
        matching_xsd_dict = None
        for xsd_name, xsd_dict in xsd_dicts.items():
            xsd_name_modified = xsd_name[1:].split('_')[0]
            #print(xsd_name_modified)
            if xsd_name_modified in col:
                matching_xsd_dict = xsd_dict
                #print("**")
                break

        if matching_xsd_dict:
            #merged_dataframe[col] = merged_dataframe[col].map(lambda x: matching_xsd_dict.get((x), x))
            ####
            #merged_dataframe[col] = merged_dataframe[col].map(matching_xsd_dict).fillna(merged_dataframe[col])
            #print("######")
            #print(col)
            #print(matching_xsd_dict)
            #print(merged_dataframe[col])
            #print("######")
            #merged_dataframe.replace({col: matching_xsd_dict},inplace=True)
            merged_dataframe[col] = merged_dataframe[col].astype(str).replace(matching_xsd_dict)
            #print(merged_dataframe[col])
    return merged_dataframe


def correlation_matrix(df):
    df_numeric = df.apply(pd.to_numeric, errors='coerce')
    correlation_matrix = df_numeric.set_index(['PcrKey']).corr()
    return correlation_matrix

def scatter_plots(corr,df):
    # Generate scatter plots for the correlated pairs
    for pair in corr.index:
        x, y = pair
        if x != y:
            plt.figure(figsize=(6, 4))
            sns.scatterplot(data=df, x=x, y=y)
            plt.title(f'Scatter Plot for {x} vs {y}')
            plt.xlabel(x)
            plt.ylabel(y)
            plt.show()

if __name__ == '__main__':
    unzip_to_folder("data/processeddataCA.zip", "data/processeddataCA")
    computedElements_dataframe,pub_PCRevents_dataframe = extract_primary_data()
    merged_dataframe = combinePrimaryDfs(computedElements_dataframe,pub_PCRevents_dataframe)
    xsd_dicts = load_XSD_Dictionary()

    dfs_dict = extract_data()
    merged_dataframe = combineDfs(merged_dataframe,dfs_dict)

    ####
    #merged_dataframe = merged_dataframe.apply(pd.to_numeric, errors='ignore')

    merged_dataframe_updated = updateCodes(merged_dataframe,xsd_dicts)
    #print(xsd_dicts['eArrest_v3.xsd'])
    print(merged_dataframe_updated.head)
    merged_dataframe_updated.to_csv(os.path.abspath("") + "/data/combined_data.csv", index=False)

    ### Uncomment below to view co-related pairs and graphs

    #computedElements_dataframe.drop(columns=computedElements_dataframe.columns[0], axis=1, inplace=True)
    #correlation_matrix = correlation_matrix(merged_dataframe_updated)
    #print(correlation_matrix)


    # Find the top 50 highest and lowest correlated pairs
    #top_50_highest_corr = correlation_matrix.unstack().sort_values(ascending=False).head(100)
    #top_50_lowest_corr = correlation_matrix.unstack().sort_values().head(50)

    #print("Top 50 Highest Correlation Pairs:")
    #print(top_50_highest_corr)

    #print("\nTop 50 Lowest Correlation Pairs:")
    #print(top_50_lowest_corr)


    #scatter_plots(top_50_highest_corr,merged_dataframe_updated)
    #scatter_plots(top_50_lowest_corr,merged_dataframe_updated)



