"""
CODE PURPOSE: 
To update the data in the file before import to system

FLOW:
1. Check for missing file
2. Read and filter only required column
3. Populate new column according to file name

"""
# import module
from datetime import datetime
import warnings
import os
import logging
import time
import pandas as pd


# logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# suppressing warning for excel style
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')


# create date format in YYYY-MM-DD for current year
def current_date_format():
    current_date = datetime.now()
    date_format = current_date.strftime('%Y-%m-%d')
    return date_format


def process_data2(folder_path, filename, date):

    file_path = os.path.join(folder_path, filename)
    # read file
    df = pd.read_excel(file_path)
    
    # filter for only pledge id column
    df = df[['Pledge ID']]
    
    df.rename(columns={'Pledge ID': 'Id'}, inplace=True)
    
    # populate column with date, status, and closed reason accordingly. 
    df['npsp__EndDate__c'] = date
    df['npsp__Status__c'] = ''
    df['npsp__ClosedReason__c'] = ''

    if 'Burnt' in filename:
        df['npsp__Status__c'] = 'Burnt'
        df['npsp__ClosedReason__c'] = 'Burnt'
    elif 'Rejected' in filename:
        df['npsp__Status__c'] = 'Rejected'
        df['npsp__ClosedReason__c'] = 'Soft Reject'

    # save the file
    df.to_excel(os.path.join(folder_path, f'{filename[:-25]}_to_upload.xlsx'), index=False)
    

def task_set_reject_burnt():

    logging.info('Start process')
    start_time = time.time()

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\2 Areas\To Set Reject and Burnt Status\2025\May\Test'
    directory = os.listdir(folder_path)
    
    date = current_date_format()

    file_keyword = ['MCO To Burnt Report', 'MCO To Rejected Report']

    logging.info('Check for missing file')
    # create dictionary with all keys from process info dictionary and assign none value
    found_files = {key: None for key in file_keyword}

    # iterate over directory and keyword list
    for file in directory:
        for keyword in file_keyword:
            if keyword in file:
                found_files[keyword] = file
                break # to stop inner loop and move to next file
    
    # check dictionary for missing value
    if not all(found_files.values()):
        missing = [key for key, val in found_files.items() if val is None]
        logging.error(f"Missing required files: {', '.join(missing)}")
        return # stop processing when file missing.
    
    for file in directory:
        
        process_data2(folder_path, file, date)
        logging.info(f'{file} has been processed')
    
    elapsed_time = time.time() - start_time
    logging.info(f'Process Completed. Elapsed time : {elapsed_time:.2f} seconds.')    


if __name__ == '__main__':
    task_set_reject_burnt()

