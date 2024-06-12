# import from local module
from .mobile_phone_handler import process_mobile_numbers, delete_condition
from .duplication_handler import remove_duplicates
from .helper_for_uts_format import create_uts_table
from .helper_upgrade import copy_data_upgrade

# import from library
from datetime import datetime
import pandas as pd
import os

def rename_file(file):
    # get current date
    current_date = datetime.now() # get current date
    date_format = current_date.strftime('%Y%m%d') # reformat date

    prefix = file[:-25]
    return f'{prefix}_{date_format}.xlsx'

def process_file(folder_path, file):
    # get file path based on join folder path and file name
    file_path = os.path.join(folder_path, file)

    # read excel file
    original_df = pd.read_excel(file_path)

    # run function
    updated_df = create_uts_table()
    updated_df = copy_data_upgrade(updated_df, original_df)

    # clean phone number in column
    updated_df = process_mobile_numbers(updated_df, 'Mobile Phone')

    # exclude invalid number rows and assign to new dataframe
    rows_to_exclude = delete_condition(updated_df, 'Mobile Phone')
    excluded_df = updated_df[rows_to_exclude]

    # use opposite condition to filter the wanted number
    rows_to_update = ~ rows_to_exclude
    updated_df = updated_df[rows_to_update]

    # delete duplicate based on mobile phone column
    updated_df = remove_duplicates(updated_df, 'Mobile Phone')

    # rename the file, build new file path, save file
    new_file_name = rename_file(file)
    new_file_path = os.path.join(folder_path, new_file_name)
    updated_df.to_excel(new_file_path, index=False)

    return original_df, updated_df, excluded_df, new_file_name