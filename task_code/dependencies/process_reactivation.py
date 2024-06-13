# import from local module
from .helper_date import current_date_format_YYYYMMDD
from .helper_for_uts_format import create_uts_table
from .helper_reactivation import copy_data_reactivation
from .helper_mobile_phone import process_mobile_numbers, delete_condition
from .helper_duplication import remove_duplicates

# import from library
import pandas as pd
import os

batch_counter = 1

def reset_batch_counter():
    global batch_counter
    batch_counter = 1

def generate_file_name(file_path, date_format):
    global batch_counter
    prefix = None

    if 'DL' in file_path and 'Reject' in file_path:
        prefix = 'TMDL_XR'
    elif 'DL' in file_path and 'Cancel' in file_path:
        prefix = 'TMDL_XC'
    elif 'RL' in file_path and 'Reject' in file_path:
        prefix = 'TMRL_XR'
    elif 'RL' in file_path and 'Cancel' in file_path:
        prefix = 'TMRL_XC'
    else:
        print(f'failed to print prefix for this path : {file_path}')

    new_file_name = f'{prefix}_Batch{batch_counter}_{date_format}.xlsx'
    batch_counter += 1

    return new_file_name

def assign_campaign(file_path, df):
    if 'DL' in file_path and 'Reject' in file_path:
        df['Campaign'] = '7015g000000pFPL'
        df['Campaign Name'] = 'TM Deeply Lapsed Reactivation (Rejected)'
        df['Description'] = 'TM Deeply Lapsed Reactivation (Rejected)'

    elif 'DL' in file_path and 'Cancel' in file_path:
        df['Campaign'] = '7015g000000pEbX'
        df['Campaign Name'] = 'TM Deeply Lapsed Reactivation (Cancelled)'
        df['Description'] = 'TM Deeply Lapsed Reactivation (Cancelled)'
    
    elif 'RL' in file_path and 'Reject' in file_path:
        df['Campaign'] = '7015g000000pFPQAA2'
        df['Campaign Name'] = 'TM Lapsed Pledge Reactivation (Rejected)'
        df['Description'] = 'TM Lapsed Pledge Reactivation (Rejected)'
        
    elif 'RL' in file_path and 'Cancel' in file_path:
        df['Campaign'] = '7015g000000pEbQ'
        df['Campaign Name'] = 'TM Lapsed Pledge Reactivation (Cancelled)'
        df['Description'] = 'TM Lapsed Pledge Reactivation (Cancelled)'

    else:
        print('Cannot assign Campaign')

    return df

# function to process file
def process_files(file_path, subfolder_path):

    # read file
    original_df = pd.read_excel(file_path, dtype={'Mailing Zip/Postal Code': str})

    # build df with uts column format
    updated_df = create_uts_table()

    # copy data from old format to new format
    updated_df = copy_data_reactivation(updated_df, original_df)

    # reformat phone number
    updated_df = process_mobile_numbers(updated_df, 'Mobile Phone')

    # use condition to filter rows to be excluded and build df
    rows_to_exclude = delete_condition(updated_df, 'Mobile Phone')
    excluded_df = updated_df[rows_to_exclude]

    # use opposite condition to filter the wanted rows and build df
    rows_to_update = ~ rows_to_exclude
    updated_df = updated_df[rows_to_update]

    # remove duplicate based on column
    updated_df = remove_duplicates(updated_df, 'Mobile Phone')

    # populate campaign column
    updated_df = assign_campaign(file_path, updated_df)

    # get date format
    date_format = current_date_format_YYYYMMDD()

    # rename file and save file
    new_file_name = generate_file_name(file_path, date_format)
    new_file_path = os.path.join(subfolder_path, new_file_name)
    updated_df.to_excel(new_file_path, index=False)

    # return these 4 variable to be used in main function
    return original_df, updated_df, excluded_df, new_file_name