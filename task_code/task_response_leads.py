# import dependencies
from dateutil.relativedelta import relativedelta
from datetime import datetime
from tabulate import tabulate
import pandas as pd
import warnings
import logging
import time
import os


def rename_file(file):
    # get extracted name from original file name
    extracted_name = file[19:]

    # get current date and reformat them
    current_date = datetime.now()
    date_format = current_date.strftime('%y%m%d')
    
    # to get previous month text in 3 letter form
    previous_month = current_date - relativedelta(months=1)
    previous_month_text = previous_month.strftime('%b')

    # rename the file
    new_file_name = f'MCO_UTS_RESPONSE_{date_format}_{previous_month_text}{extracted_name}'

    return new_file_name

def task_response_leads_main(folder_path):
    # add start time to record code runtime
    start_time = time.time()

    # ignore warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    logging.info('Processing Response Leads file...')

    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_response_leads\test_data\Mar'

    # check if the file with selected name has been process
    if not any('MCO_UTS' in file for file in os.listdir(folder_path)):

        logging.info('Checking existing file...')
        logging.info('No existing file detected. Process continue...')

        # initialize list for saving file data
        processed_file_info = []

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            # to preserve data with leading zero in these columns
            columns_with_leading_zero = ['Post Code', 'Donation Amount', 'Home Phone', 'Work Phone', 'Mobile Phone']
            # change dtype to str
            dtype_dict = {column : str for column in columns_with_leading_zero}

            # read file
            original_df = pd.read_excel(file_path, dtype=dtype_dict)

            # filter out column data = subscribe
            updated_df = original_df[original_df['Description'] != 'Subscribe']

            # applied rename file function
            new_file_name = rename_file(file)   

            # build file path for new file
            new_file_path = os.path.join(folder_path, new_file_name)

            # save file
            updated_df.to_excel(new_file_path, index=False)

            # get data into list
            processed_file_info.append({
                'File Name' : new_file_name, # get file name
                'Before Clean' : len(original_df), # count before clean
                'After Clean' : len(updated_df) # count after clean
            }) 

        # print completion status
        logging.info('Process completed!. Files has been saved in selected folder.')
        logging.info('Here is the file analysis for your reference.')
        # print a table to show list
        logging.info(tabulate(processed_file_info, headers="keys", tablefmt="grid")) 
    else:
        logging.info('Files already been processed! Please check the folder')  

    # get end time for runtime and print
    end_time = time.time()
    code_runtime = end_time - start_time
    logging.info('Processing Time: {:2f} seconds'.format(code_runtime))