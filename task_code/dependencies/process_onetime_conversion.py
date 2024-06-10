# import module
from datetime import datetime
from tabulate import tabulate
import pandas as pd
import os

from .mobile_phone_handler import process_mobile_numbers, delete_condition
from .duplication_handler import remove_duplicates


def rename_file():
    current_date = datetime.now()
    date_format = current_date.strftime('%Y%m%d')
    new_file_name = f'TMOC_UTS_{str(date_format)}.xlsx'
    return new_file_name

def process_file(folder_path, file_name):
    # get path
    file_path = os.path.join(folder_path, file_name)

    # read file and make postcode column a string
    original_df = pd.read_excel(file_path, dtype={'Post Code': str})
    
    # assign df to new variable
    updated_df = original_df
    
    # clean phone number in column
    updated_df = process_mobile_numbers(updated_df, 'Mobile Phone')

    # exclude invalid number rows and assign to new dataframe
    rows_to_exclude = delete_condition(updated_df, 'Mobile Phone')
    excluded_df = updated_df[rows_to_exclude]

    # use opposite condition to filter the wanted number
    rows_to_update = ~ rows_to_exclude
    updated_df = updated_df[rows_to_update]

    # remove duplicate based on column
    updated_df = remove_duplicates(updated_df, 'Mobile Phone')

    # rename file using function, build new file path and save file
    new_file_name = rename_file()
    new_file_path = os.path.join(folder_path, new_file_name)
    updated_df.to_excel(new_file_path, index=False)

    return original_df, updated_df, excluded_df, new_file_name



    