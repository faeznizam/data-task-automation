import pandas as pd
from datetime import datetime
import os

def read_file(file_path):
    df = pd.read_excel(file_path, dtype={'Post Code' : str})

    return df


def populate_campaign(df, file):
    if 'HR' in file:
        df['Campaign'] = '7015g000000pEcvAAE'
        df['Campaign Name'] = 'OnHold UTS HR'
        df['Description'] = 'OnHold UTS HR'

    elif 'SR' in file:
        df['Campaign'] = '7015g000000pEqfAAE'
        df['Campaign Name'] = 'OnHold UTS SR'
        df['Description'] = 'OnHold UTS SR'
    
    return df

def remove_duplicates(df):
    column_to_check_duplicate = 'Mobile Phone'
    df.drop_duplicates(subset = column_to_check_duplicate, keep = 'first', inplace = True)

    return df

def rename_uts_file(file):

    current_date = datetime.now()
    date_format = current_date.strftime('%y%m%d')
    extract_file_number = file[-7:-5]
    
    if 'HR' in file:
        return f'TM_UTS_HR_OH{extract_file_number}_{date_format}.xlsx'
    elif 'SR' in file:
        return f'TM_UTS_SR_OH{extract_file_number}_{date_format}.xlsx'
    else:
        pass


def save_file(df, new_filename, folder_path):
    new_file_path = os.path.join(folder_path, new_filename)
    df.to_excel(new_file_path, index=False)

    print(f'{new_filename} has been saved in the folder')