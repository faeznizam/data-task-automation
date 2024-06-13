# import from local module
from .helper_mobile_phone import process_mobile_numbers, delete_condition
from .helper_duplication import remove_duplicates

# import from library
from datetime import datetime
import pandas as pd
import os

def rename_file(file):
    current_date = datetime.now() # get current date
    date_format = current_date.strftime('%Y%m%d') # reformat date

    return f'TM_{file[8:11]}{file[12:15]}_{file[16:18]}_OH{file[19:21]}_{date_format}.xlsx'

def process_file(subfolder_path, file):

    file_path = os.path.join(subfolder_path, file)

    original_df = pd.read_excel(file_path, dtype={'Post Code': str})

    updated_df = original_df

    updated_df = process_mobile_numbers(updated_df, 'Mobile Phone')

    # exclude invalid number rows and assign to new dataframe
    rows_to_exclude = delete_condition(updated_df, 'Mobile Phone')
    excluded_df = updated_df[rows_to_exclude]

    # use opposite condition to filter the wanted number
    rows_to_update = ~ rows_to_exclude
    updated_df = updated_df[rows_to_update]

    updated_df = remove_duplicates(updated_df, 'Mobile Phone')

    new_file_name = rename_file(file)
    new_file_path = os.path.join(subfolder_path, new_file_name)

    updated_df.to_excel(new_file_path, index=False)

    return original_df, updated_df, excluded_df, new_file_name

