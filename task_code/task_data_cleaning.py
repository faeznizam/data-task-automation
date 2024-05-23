# import from sub files
from dependencies import clean_gender
from dependencies import clean_icnumber
from dependencies import clean_birthdate
from dependencies import clean_email
from dependencies import clean_ethnic
from dependencies import clean_phone_number
from dependencies import clean_file_name

# import from module
import pandas as pd
import os
import warnings
from datetime import datetime
import logging


def create_file_path(folder_path, file):
    return os.path.join(folder_path, file)

def create_date_format():
    current_date = datetime.now()
    date_format = current_date.strftime('%Y-%m-%d')
    return date_format

def rename_file(file, date_format):
    extract_filename = file[:-5]
    new_file_name = f'{extract_filename}_{date_format}.xlsx'
    return new_file_name

def save_file(folder_path, new_file_name, df):
    file_path = os.path.join(folder_path, new_file_name)
    df.to_excel(file_path, index=False)
    print(f'{new_file_name} has been saved in the folder!')

def convert_date_format(df):
    df['Created Date'] = pd.to_datetime(df['Created Date'], format='%d/%m/%Y')
    df['Created Date'] = df['Created Date'].dt.strftime('%Y-%m-%d')

    return df

def task_data_cleaning_main(folder_path):

    logging.info("Start data cleaning process...")

    # ignore warning
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')
    # clean timestamp in file name
    clean_file_name.clean_name(folder_path)
    # create data formatting
    date_format = create_date_format()

    # iterate the folder
    for file in os.listdir(folder_path):

        if 'Donor With Invalid Email.xlsx' in file:
            # build file path
            file_path = create_file_path(folder_path, file)
            # read the file
            df = pd.read_excel(file_path)

            # process the file
            df = clean_email.rename_column(df)
            df['Email'] = df['Original Email'].apply(clean_email.check_email)
            df['npe01__HomeEmail__c'] = df['Original Email'].apply(clean_email.check_email)
            df['npe01__Preferred_Email__c'] = df['Original Email'].apply(clean_email.check_email)
            df['npe01__WorkEmail__c'] = df['Original Email'].apply(clean_email.check_email)
            df['Date'] = create_date_format()

            # rename and save the file
            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)

            logging.info('Email file has been cleaned.')

        elif 'Donor With Invalid IC.xlsx' in file:
            # building file path
            file_path = create_file_path(folder_path, file)
            # read the file
            df = pd.read_excel(file_path, dtype = {'National ID': str})

            # process the file
            df['Updated National ID'] = df['National ID'].apply(clean_icnumber.validate_nat_id)
            df = clean_icnumber.blank_invalid_ic(df)
            df = clean_icnumber.rename_column(df)
            df['Date'] = create_date_format()

            # rename and save the file
            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)

            logging.info('IC file has been cleaned.')

        elif 'Donor With Invalid Phone Number.xlsx' in file:
            # build file path and read the file
            file_path = create_file_path(folder_path, file)
            df = pd.read_excel(file_path)

            # clean the data
            df = clean_phone_number.process_mobile_numbers(df)
            df = clean_phone_number.rename_column(df)
            df['Date'] = create_date_format()

            # rename and save the data
            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)

            logging.info('Phone Number file has been cleaned.')

        elif 'Donor Without Age and Birthdate.xlsx' in file:
            # build file path and read the file
            file_path = create_file_path(folder_path, file)
            df = pd.read_excel(file_path, dtype = {'National ID': str})

            # clean the data
            df['National ID'] = df['National ID'].apply(clean_birthdate.validate_nat_id)
            df['Birthdate'] = df['National ID'].apply(clean_birthdate.calculate_birthdate)
            df['Age'] = df['Birthdate'].apply(clean_birthdate.calculate_age)
            df['Date'] = create_date_format()

            # rename and save the file
            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)

            logging.info('Birthdate file has been cleaned.')
            
        elif 'Donor Without Ethnic.xlsx' in file:
            # build file path and read the file
            file_path = create_file_path(folder_path, file)
            df = pd.read_excel(file_path)

            # clean the data
            df['Ethnic'] = df['Full Name'].apply(clean_ethnic.categorize_ethnic)
            df = clean_ethnic.rename_column(df)
            df['Date'] = create_date_format()

            # rename and save the file
            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)

            logging.info('Ethnic file has been cleaned.')

        elif 'Donor Without Gender.xlsx' in file:
            # build file path and rename file
            file_path = create_file_path(folder_path, file)
            df = pd.read_excel(file_path, dtype = {'National ID': str})

            # clean the data
            df['National ID'] = df['National ID'].apply(clean_icnumber.validate_nat_id)
            df = clean_gender.gender_by_national_id(df)
            df = clean_gender.rename_column(df)
            df['Date'] = create_date_format()
            
            # rename and save the data
            date_format = create_date_format()
            df = convert_date_format(df)
            new_file_name = rename_file(file, date_format)
            save_file(folder_path, new_file_name, df)

        else:
            pass







