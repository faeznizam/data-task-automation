import pandas as pd
import os
import warnings
from tabulate import tabulate

from script import remove_duplicate
from script import clean_phone_number




def main(folder_path):
    # filter warning 
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        for file in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, file)

            df = pd.read_excel(file_path, dtype={'Post Code' : str})

            cleaned_df = clean_phone_number.process_mobile_numbers(df)

            cleaned_df = remove_duplicate.remove_duplicates(df)

            cleaned_df.to_excel(file_path, index=False)

            print(f'{file} has been save in the folder')


    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        for file in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, file)
            
            df = pd.read_excel(file_path)

            print(f'File: {file} , Number of Rows: {len(df)} , Inv no count: {clean_phone_number.count_invalid_number(df)}')
    
    




