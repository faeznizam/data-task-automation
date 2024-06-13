# import from local module
from .helper_startek import create_startek_table, copy_data_startek, populate_pkg_column
from .helper_mobile_phone import process_mobile_numbers, delete_condition
from .helper_duplication import remove_duplicates

# import from library
from datetime import datetime
import pandas as pd
import os

def rename_startek_file(file):
    current_date = datetime.now()
    date_format = current_date.strftime('%y%m%d')
    extract_file_number = file[-7:-5]
    
    if 'HR' in file:
        return f'TM_AG_HR_OH{extract_file_number}_{date_format}.xlsx'
    elif 'SR' in file:
        return f'TM_AG_SR_OH{extract_file_number}_{date_format}.xlsx'
    else:
        pass

# function for different process
def process_startek(sub_folder_path, file):
   
   file_path = os.path.join(sub_folder_path, file)
   
   # read file
   original_df = pd.read_excel(file_path, dtype={'Post Code': str})

   # initialize new dataframe with new format and move data to new dataframe
   updated_df = create_startek_table()
   updated_df = copy_data_startek(updated_df, original_df)
   updated_df = populate_pkg_column(file, updated_df)

   # clean phone number column
   updated_df = process_mobile_numbers(updated_df, 'PH_CELL')

   # exclude invalid number rows and assign to new dataframe
   rows_to_exclude = delete_condition(updated_df, 'PH_CELL')
   excluded_df = updated_df[rows_to_exclude]

   # use opposite condition to filter the wanted number
   rows_to_update = ~ rows_to_exclude
   updated_df = updated_df[rows_to_update]

   # delete duplicate based on phone number column
   updated_df = remove_duplicates(updated_df, 'PH_CELL')

   # rename file and save file
   new_file_name = rename_startek_file(file)
   new_file_path = os.path.join(sub_folder_path, new_file_name)
   updated_df.to_excel(new_file_path, index=False)

   return original_df, updated_df, excluded_df, new_file_name



