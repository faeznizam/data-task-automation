from .helper_duplication import remove_duplicates
from .helper_mobile_phone import process_mobile_numbers, delete_condition

from datetime import datetime
import pandas as pd
import os

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

def process_file(folder_path, file):
    # get file path
    file_path = os.path.join(folder_path, file)

    # read file
    original_df = pd.read_excel(file_path, dtype={'Post Code': str})
    # save df to modified in new variable
    updated_df = original_df
    # clean phone number
    updated_df = process_mobile_numbers(updated_df, 'Mobile Phone')
    
    # exclude invalid number rows and assign to new dataframe
    rows_to_exclude = delete_condition(updated_df, 'Mobile Phone')
    excluded_df = updated_df[rows_to_exclude]

    # use opposite condition to filter the wanted number
    rows_to_update = ~ rows_to_exclude
    updated_df = updated_df[rows_to_update]

    # remove duplicate
    updated_df = remove_duplicates(updated_df, 'Mobile Phone')
    
    # rename file using function, build new file path and save file
    new_file_name = rename_file(file)
    new_file_path = os.path.join(folder_path, new_file_name)
    updated_df.to_excel(new_file_path, index=False)

    return original_df, updated_df, excluded_df, new_file_name

