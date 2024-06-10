# import dependency
from datetime import datetime
from tabulate import tabulate
import pandas as pd
import os

from .mobile_phone_handler import process_mobile_numbers, delete_condition
from .helper_burnt import create_uts_table, copy_data_to_new_table
from .duplication_handler import remove_duplicates


def rename_file():
    current_date = datetime.now() # get current date
    date_format = current_date.strftime('%Y%m%d') # reformat date
    new_file_name = f'TMBN_XB_UTS_{str(date_format)}.xlsx'
    return new_file_name

def process_file(folder_path, file_name):
    # get file path based on join folder path and file name
    file_path = os.path.join(folder_path, file_name)

    # read the excel file and set mailing zip and postal code to have string data type
    original_df = pd.read_excel(file_path, dtype={'Mailing Zip/Postal Code': str})

    # run function
    updated_df = create_uts_table()
    updated_df = copy_data_to_new_table(updated_df, original_df)

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
    new_file_name = rename_file()
    new_file_path = os.path.join(folder_path, new_file_name)
    updated_df.to_excel(new_file_path, index=False)

    return original_df, updated_df, excluded_df, new_file_name
