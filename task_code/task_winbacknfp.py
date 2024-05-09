import pandas as pd
import warnings
import os
from datetime import datetime
from tabulate import tabulate

from dependencies import clean_phone_number
from dependencies import remove_duplicate

def rename_file(file):
    # get current date
    current_date = datetime.now() # get current date
    date_format = current_date.strftime('%Y%m%d') # reformat date

    # rename the file based on filename
    if 'BSN - HR' in file:
        new_filename = f'TMNFP_BSN_HR_{date_format}.xlsx'
    elif 'BSN - SR' in file:
        new_filename = f'TMNFP_BSN_SR_{date_format}.xlsx'
    elif 'RHB - HR' in file:
        new_filename = f'TMNFP_RHB_HR_{date_format}.xlsx'
    elif 'RHB - SR' in file:
        new_filename = f'TMNFP_RHB_SR_{date_format}.xlsx'

    return new_filename

def main(folder_path):
    # remove warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    # check if the file with selected name has been process
    if not any('TMNFP' in file for file in os.listdir(folder_path)):
        
        # initialize list for saving file data
        processed_file_info = []

        # iterate over every file in the folder
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            # read file
            df = pd.read_excel(file_path, dtype={'Post Code': str})
            # save df to modified in new variable
            modified_df = df
            # clean phone number
            modified_df = clean_phone_number.process_mobile_numbers(modified_df)
            # remove duplicate
            modified_df = remove_duplicate.remove_duplicates(modified_df, 'Mobile Phone')
            # rename file
            new_file_name = rename_file(file)
            # get new path
            new_file_path = os.path.join(folder_path, new_file_name)
            # save file
            modified_df.to_excel(new_file_path, index=False)

            # get data into list
            processed_file_info.append({
                'File Name' : new_file_name, # get file name
                'Before Clean' : len(df), # count before clean
                'After Clean' : len(modified_df), # count after clean
                'Invalid Phone Number' : clean_phone_number.count_invalid_phone_number(modified_df, 'Mobile Phone') # flag invalid mobile number
            }) 

        # print completion status
        print('Process completed.')
        # print the list in table form
        print(tabulate(processed_file_info, headers="keys", tablefmt="grid"))

    else:
        print('Files already been processed! Please check the folder')  


