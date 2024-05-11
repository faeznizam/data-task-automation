# import module from folder
from .dependencies import clean_phone_number, burnt_subfile, remove_duplicate

# import dependency
from datetime import datetime
from tabulate import tabulate
import pandas as pd
import warnings
import logging
import time
import os


def rename_file():
    current_date = datetime.now() # get current date
    date_format = current_date.strftime('%Y%m%d') # reformat date
    new_file_name = f'TMBN_XB_UTS_{str(date_format)}.xlsx'
    return new_file_name

def task_burnt_main(folder_path):
    # add start time to record code runtime
    start_time = time.time()
    # Ignore warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_burnt\test_data'
    
    # check if files has been processed
    if not any('TMBN' in file for file in os.listdir(folder_path)):

        logging.info('Checking existing file...')
        logging.info('No existing file detected. Process continue...')

        # initialize list to get data
        processed_file_info = []
        deleted_list = []

        # iterate files in folder
        for file_name in os.listdir(folder_path):
            
            if 'Burnt Report' in file_name:
                
                # get file path based on join folder path and file name
                file_path = os.path.join(folder_path, file_name)

                # read the excel file and set mailing zip and postal code to have string data type
                original_df = pd.read_excel(file_path, dtype={'Mailing Zip/Postal Code': str})

                # run function
                updated_df = burnt_subfile.initalize_uts_file_format()
                updated_df = burnt_subfile.copy_data(updated_df, original_df)

                # clean phone number in column
                updated_df = clean_phone_number.process_mobile_numbers(updated_df)

                # exclude invalid number rows and assign to new dataframe
                rows_to_exclude = clean_phone_number.delete_condition(updated_df, 'Mobile Phone')
                excluded_df = updated_df[rows_to_exclude]

                # use opposite condition to filter the wanted number
                rows_to_update = ~ rows_to_exclude
                updated_df = updated_df[rows_to_update]

                # delete duplicate based on mobile phone column
                updated_df = remove_duplicate.remove_duplicates(updated_df, 'Mobile Phone')

                # rename the file, build new file path, save file
                new_file_name = rename_file()
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
