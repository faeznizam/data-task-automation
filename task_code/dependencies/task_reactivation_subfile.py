import pandas as pd
from datetime import datetime
import os


def read_file(file_path):

    df = pd.read_excel(file_path, dtype={'Mailing Zip/Postal Code': str})

    return df

    
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

def get_current_date():
    current_date = datetime.now() # get current date
    date_format = current_date.strftime('%Y%m%d') # reformat date

    return date_format

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

def save_file(subfolder_path, new_file_name, new_df):
    new_file_path = os.path.join(subfolder_path, new_file_name)
    new_df.to_excel(new_file_path, index=False)
    

