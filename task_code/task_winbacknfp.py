# import module from folder
from .dependencies import mobile_phone_handler, duplication_handler

# import dependencies
from datetime import datetime
from tabulate import tabulate
import pandas as pd
import warnings
import logging
import time
import os


def rename_file(file):
    # get current date
    current_date = datetime.now() # get current date
    date_format = current_date.strftime('%Y%m%d') # reformat date

    # rename the file based on filename
    if 'BSN - HR' in file:
        new_filename = f'TMNFP_BSN_HR_{date_format}.xlsx'
    elif 'BSN - SR' in file:
        new_filename = f'TMNFP_BSN_SR_{date_format}.xlsx'
    elif 'RHB - HR' in file:
        new_filename = f'TMNFP_RHB_HR_{date_format}.xlsx'
    elif 'RHB - SR' in file:
        new_filename = f'TMNFP_RHB_SR_{date_format}.xlsx'

    return new_filename

def task_winbacknfp_main(folder_path):
    # add start time to record code runtime
    start_time = time.time()

    # ignore warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    logging.info('Processing Winback No First Payment file...')

    # check if the file with selected name has been process
    if not any('TMNFP' in file for file in os.listdir(folder_path)):

        logging.info('Checking existing file...')
        logging.info('No existing file detected. Process continue...')

        
        # initialize list for saving file data
        processed_file_info = []
        deleted_list = []

        # iterate over every file in the folder
        for file in os.listdir(folder_path):
            # get file path
            file_path = os.path.join(folder_path, file)

            # read file
            original_df = pd.read_excel(file_path, dtype={'Post Code': str})
            # save df to modified in new variable
            updated_df = original_df
            # clean phone number
            updated_df = mobile_phone_handler.process_mobile_numbers(updated_df, 'Mobile Phone')
            
            # exclude invalid number rows and assign to new dataframe
            rows_to_exclude = mobile_phone_handler.delete_condition(updated_df, 'Mobile Phone')
            excluded_df = updated_df[rows_to_exclude]

            # use opposite condition to filter the wanted number
            rows_to_update = ~ rows_to_exclude
            updated_df = updated_df[rows_to_update]
        
            # remove duplicate
            updated_df = duplication_handler.remove_duplicates(updated_df, 'Mobile Phone')
            
            # rename file using function, build new file path and save file
            new_file_name = rename_file(file)
            new_file_path = os.path.join(folder_path, new_file_name)
            updated_df.to_excel(new_file_path, index=False)

            # check if the df is not empty then append to deleted_list
            if not excluded_df.empty:
                # add file name so that I know where the row belongs
                excluded_df['File Name'] = new_file_name
                deleted_list.append(excluded_df)

            # get data into list
            processed_file_info.append({
                'File Name' : new_file_name, # get file name
                'Before Clean' : len(original_df), # count before clean
                'After Clean' : len(updated_df), # count after clean
            }) 

        # combine all df that has been append to list and save the file in excel
        # empty list gave out False boolean
        if deleted_list:
            final_deleted_df = pd.concat(deleted_list, ignore_index=True)
            final_deleted_df.to_excel(os.path.join(folder_path, 'deleted_list.xlsx'), index=False)
        else:
            logging.info('Deleted list was not created since there is no data!')

        # print process status and analysis
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