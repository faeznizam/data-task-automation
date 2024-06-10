# import from sub files

from .dependencies import (
    clean_gender,clean_icnumber, clean_birthdate, clean_email, clean_ethnic, 
    clean_phone_number, clean_file_name, date_handler
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

def process_file(file, folder_path, date_format, clean_function):
    file_path = create_file_path(folder_path, file)
    df = pd.read_excel(file_path)

    # check if national id column exist
    if 'National ID' in df.columns:
        df['National ID'] = df['National ID'].astype(str)

    # process function
    df = clean_function(df)

    df['Date'] = date_format

    # change date format in one of the column
    df = date_handler.convert_date_format(df)
    new_file_name = rename_file(file, date_format)
    new_file_path = create_file_path(folder_path, new_file_name)
    df.to_excel(new_file_path, index=False)

    logging.info(f'{new_file_name} has been created. ')
    
def task_data_cleaning_main(folder_path):

    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_data_cleaning'

    # ignore warning
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')
    # remove timestamp in file name
    clean_file_name.remove_timestamp(folder_path)

    # get current date in YYYY-MM-DD format
    date_format = date_handler.current_date_format()

    file_cleaning_map = {
        'Donor With Invalid Email.xlsx' : clean_email.clean_email_file, 
        'Donor With Invalid IC.xlsx' : clean_icnumber.clean_ic_file,
        'Donor With Invalid Phone Number.xlsx' : clean_phone_number.clean_phone_file, 
        'Donor Without Age and Birthdate.xlsx' : clean_birthdate.clean_birthdate_file,
        'Donor Without Ethnic.xlsx' : clean_ethnic.clean_ethnic_file,
        'Donor Without Gender.xlsx' : clean_gender.clean_gender_file 

    }

    for file in os.listdir(folder_path):
        if file in file_cleaning_map:
            process_file(file, folder_path, date_format, file_cleaning_map[file])
        


"""
if __name__ == '__main__':
    task_data_cleaning_main()

"""