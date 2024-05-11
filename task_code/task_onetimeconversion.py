# import module from folder
from .dependencies import clean_phone_number
from .dependencies import remove_duplicate

# import dependencies
import pandas as pd
from datetime import datetime
import os
import warnings
from tabulate import tabulate
import time
import logging


def rename_file():
    current_date = datetime.now()
    date_format = current_date.strftime('%Y%m%d')
    new_file_name = f'TMOC_UTS_{str(date_format)}.xlsx'
    return new_file_name

def task_onetimeconversion_main(folder_path):
    # add start time to record code runtime
    start_time = time.time()

    # ignore warnings
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')
    warnings.filterwarnings("ignore", category=FutureWarning)

    logging.info('Processing One Time Conversion To Pledge file...')

    # check if files already been processed
    if not any('TMOC' in file for file in os.listdir(folder_path)):

        logging.info('Checking existing file...')
        logging.info('No existing file detected. Process continue...')

        #Initiate list to get data
        processed_file_info = []
        deleted_list = []

        #iterate files in folder
        for file_name in os.listdir(folder_path):

            # select file using prefix and let user know if file already done
            if 'TM One Time' in file_name:

                # get file path
                file_path = os.path.join(folder_path, file_name)

                # read file and make postcode column a string
                original_df = pd.read_excel(file_path, dtype={'Post Code': str})

                # assign df to new variable
                updated_df = original_df

                # clean phone number in column
                updated_df = clean_phone_number.process_mobile_numbers(updated_df)

                # exclude invalid number rows and assign to new dataframe
                rows_to_exclude = clean_phone_number.delete_condition(updated_df, 'Mobile Phone')
                excluded_df = updated_df[rows_to_exclude]

                # use opposite condition to filter the wanted number
                rows_to_update = ~ rows_to_exclude
                updated_df = updated_df[rows_to_update]

                # remove duplicate based on column
                updated_df = remove_duplicate.remove_duplicates(updated_df, 'Mobile Phone')

                # rename file using function, build new file path and save file
                new_file_name = rename_file()
                new_file_path = os.path.join(folder_path, new_file_name)
                updated_df.to_excel(new_file_path, index=False)

                # check if the df is not empty then append to deleted_list
                if not excluded_df.empty:
                    # add file name so that I know where the row belongs
                    excluded_df['File Name'] = new_file_name
                    deleted_list.append(excluded_df)

                # append row count for before and after to list in dictionary.
                processed_file_info.append({
                    'File Name' : new_file_name,
                    'Before Clean' : len(original_df),
                    'After Clean' : len(updated_df),
                }) 

            # combine all df that has been append to list and save the file in excel
            final_deleted_df = pd.concat(deleted_list, ignore_index=True)
            final_deleted_df.to_excel(os.path.join(folder_path, 'deleted_list.xlsx'), index=False)
            
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
