import pandas as pd
import zipfile


def extract_specific_file_from_zip_archive(zip_file_path, csv_file_name):
    """
    :param zip_file_path: The path to the archive
    :param csv_file_name: The file you want extracted from the archive
    :return: A dataframe from the CSV file that is extracted from the archive

    """
    # Using the zipfile module to read the specific CSV file from the ZIP
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        with z.open(csv_file_name) as f:
            df = pd.read_csv(f)

    return df
