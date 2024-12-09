# local dependencies for the file
from .helper_mobile_phone import process_mobile_numbers, delete_condition

# import library
from datetime import datetime # to handle data time related 
import pandas as pd # to manipulate data 
import os # to interact with file system

def calculate_count_by_campaign(updated_df):
    campaign_count = updated_df.groupby('Campaign Name').size()
    return campaign_count.reset_index(name='Counts')

def create_file_name():
    current_date = datetime.now()
    date_format = current_date.strftime('%Y%m%d')
    return f'TMOC_UTS_{str(date_format)}.xlsx'

def process_file(folder_path, file_name):
    """
    To process one time conversion file

    Parameter:
    - folder path (str): file directory contain file to process.
    - file name (str) name of file to process. 

    Output:
    - original_df: original dataframe
    - updated_df: the updated dataframe
    - excluded_df: dataframe contain excluded rows
    - new_file_name: name of the newly created file

    """

    # create file path and read the file
    file_path = os.path.join(folder_path, file_name)
    original_df = pd.read_excel(file_path, dtype={'Post Code': str})
    
    # process phone number and apply delete condition to data
    updated_df = process_mobile_numbers(original_df, 'Mobile Phone')
    rows_to_exclude = delete_condition(updated_df, 'Mobile Phone')

    # use boolean indexing to exclude and update dataframe
    excluded_df = updated_df[rows_to_exclude]
    updated_df = updated_df[~rows_to_exclude]

    # remove duplicates
    updated_df.drop_duplicates(subset='Mobile Phone', inplace=True)

    # create file name, file path and save file to excel
    new_file_name = create_file_name()
    new_file_path = os.path.join(folder_path, new_file_name)
    updated_df.to_excel(new_file_path, index=False)

    return original_df, updated_df, excluded_df, new_file_name



    