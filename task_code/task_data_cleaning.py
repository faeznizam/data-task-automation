# import from sub files

from .dependencies import (
    clean_gender,clean_icnumber, clean_birthdate, clean_email, clean_ethnic, 
    clean_phone_number, clean_file_name, helper_date
    )

# import from module
import pandas as pd
import warnings
import logging
import os

def create_file_path(folder_path, file):
    # create file path
    return os.path.join(folder_path, file)

def rename_file(file, date_format):
    # rename file by getting original file and add date
    original_filename = file[:-5]
    return f'{original_filename}_{date_format}.xlsx'

def process_file(file, folder_path, date_format, cleaning_function, columns_to_keep):
    file_path = create_file_path(folder_path, file)
    df = pd.read_excel(file_path)

    # check if national id column exist
    if 'National ID' in df.columns:
        df['National ID'] = df['National ID'].astype(str)

    # process function
    df = cleaning_function(df)

    df['Date'] = date_format

    # change date format in one of the column
    df = helper_date.convert_date_format(df)
    new_file_name = rename_file(file, date_format)
    new_file_path = create_file_path(folder_path, new_file_name)
    df.to_excel(new_file_path, index=False)

    # filter out unrelated column and save in csv
    needed_columns = columns_to_keep
    filtered_df = df[needed_columns]

    filtered_df.to_csv(new_file_path.replace('.xlsx', '.csv'), index=False)
    


    logging.info(f'{new_file_name} has been created. ')
    
def task_data_cleaning_main(folder_path):
    # ignore warning
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    # remove timestamp in file name
    clean_file_name.remove_timestamp(folder_path)

    # get current date in YYYY-MM-DD format
    date_format = helper_date.current_date_format()

    file_cleaning_map = {
        'Donor With Invalid Email.xlsx' : (clean_email.clean_email_file, clean_email.columns_to_keep()), 
        'Donor With Invalid IC.xlsx' : (clean_icnumber.clean_ic_file, clean_icnumber.columns_to_keep()),
        'Donor With Invalid Phone Number.xlsx' : (clean_phone_number.clean_phone_file, clean_phone_number.columns_to_keep()), 
        'Donor Without Age and Birthdate.xlsx' : (clean_birthdate.clean_birthdate_file, clean_birthdate.columns_to_keep()),
        'Donor Without Ethnic.xlsx' : (clean_ethnic.clean_ethnic_file, clean_ethnic.columns_to_keep()),
        'Donor Without Gender.xlsx' : (clean_gender.clean_gender_file, clean_gender.columns_to_keep()) 

    }

    for file in os.listdir(folder_path):
        if file in file_cleaning_map:
            cleaning_function, columns_to_keep = file_cleaning_map[file]
            process_file(file, folder_path, date_format, cleaning_function, columns_to_keep)
        


