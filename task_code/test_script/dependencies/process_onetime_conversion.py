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

def get_row_count(original_df, updated_df, new_file_name, processed_file_info):
    # append row count for before and after to list in dictionary.
    processed_file_info.append({
        'File Name' : new_file_name,
        'Before Clean' : len(original_df),
        'After Clean' : len(updated_df),
    }) 
    
def get_deleted_info(excluded_df, deleted_list, new_file_name):

    # check if the df is not empty then append to deleted_list
    if not excluded_df.empty:
        # add file name so that I know where the row belongs
        excluded_df['File Name'] = new_file_name
        deleted_list.append(excluded_df)

def create_deleted_list(deleted_list, folder_path):
    # empty list gave out False boolean
    if deleted_list:
        final_deleted_df = pd.concat(deleted_list, ignore_index=True)
        final_deleted_df.to_excel(os.path.join(folder_path, 'deleted_list.xlsx'), index=False)
    else:
        print('No deleted list created.')

def analysis_table(processed_file_info):
    print('\n')
    print(tabulate(processed_file_info, headers="keys", tablefmt="html"))


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



    