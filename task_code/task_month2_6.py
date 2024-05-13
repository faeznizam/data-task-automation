# import module from folder
from .dependencies import duplication_handler

# import dependencies
import pandas as pd
import os
import warnings
import time
from tabulate import tabulate
import logging

def task_month2_to_6_main(folder_path):
    # get start time
    start_time = time.time()

    # Ignore SettingWithCopyWarning and openpyxl.styles.stylesheet
    pd.options.mode.chained_assignment = None
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    logging.info('Processing Month 2 - 6 file...')

    # get folder path
    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_month2_6\test_data'

    # initiate deleted list and process info
    processed_file_info = []
    deleted_list = []

    # check if files already been processed
    if not any('deleted_list' in file for file in os.listdir(folder_path)):
        
        logging.info('Checking existing file...')
        logging.info('No existing file detected. Process continue...')

        # iterate over all the file in folder
        for file in os.listdir(folder_path):
            
            # build file path
            file_path = os.path.join(folder_path, file)

            # read file
            original_df = pd.read_excel(file_path)
            updated_df = original_df

            # fill in empty cell with empty string
            updated_df = updated_df.fillna('')

            # set up condition for filtering row to delete and assign new dataframe
            rows_to_exclude = ( ~updated_df['Mailing Country'].str.lower().isin(['malaysia', 'brunei', 'brunei darussalam', 'singapore', '']) |
                        (updated_df['Mailing Zip/Postal Code'] == "") | 
                        (updated_df['Mailing Zip/Postal Code'] == '-')
                        )
            excluded_df = updated_df[rows_to_exclude]

            # use opposite condition to filter only wanted row
            rows_to_update = ~ rows_to_exclude
            updated_df = updated_df[rows_to_update]
            
            # remove duplicate based on column
            updated_df = duplication_handler.remove_duplicates(updated_df, 'Mailing Street')

            # create new file name, create path, save file
            new_file_name = f'{file[:-25]}.xlsx'
            new_file_path = os.path.join(folder_path, new_file_name)
            updated_df.to_excel(new_file_path, index=False)

            # check if the df is not empty then append to deleted list
            if not excluded_df.empty:
                # add file name to row
                excluded_df['File Name'] = new_file_name
                # append to list
                deleted_list.append(excluded_df)

            # append row count for before and after to list in dictionary.
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

        # print completion status
        logging.info('Process completed!. Files has been saved in selected folder.')
        logging.info('Here is the file analysis for your reference.')
        # print a table to show list
        logging.info('\n')
        logging.info(tabulate(processed_file_info, headers="keys", tablefmt="html")) 

    else: 
        logging.info('Files already been processed! Please check the folder') 

    # get running end time and calculate total runtime
    end_time = time.time()
    code_runtime = end_time - start_time
    logging.info('\n')
    logging.info('Processing Time: {:2f} seconds'.format(code_runtime))
