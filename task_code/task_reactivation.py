# import from sub file
from dependencies import uts_file_format, copy_data_reactivation, task_reactivation_subfile, mobile_phone_handler, duplication_handler

# import from module
from tabulate import tabulate
import pandas as pd
import warnings
import logging
import time
import os



# function to process file
def process_files(file_path):

    # read file
    original_df = task_reactivation_subfile.read_file(file_path)

    # assign df to new variable
    updated_df = original_df

    # build df with uts column format
    updated_df = uts_file_format.initalize_uts_file_format()

    # copy data from old format to new format
    updated_df = copy_data_reactivation.copy_data_reactivation(updated_df, original_df)

    # reformat phone number
    updated_df = mobile_phone_handler.process_mobile_numbers(updated_df)

    # use condition to filter rows to be excluded and build df
    rows_to_exclude = mobile_phone_handler.delete_condition(updated_df, 'Mobile Phone')
    excluded_df = updated_df[rows_to_exclude]

    # use opposite condition to filter the wanted rows and build df
    rows_to_update = ~ rows_to_exclude
    updated_df = updated_df[rows_to_update]

    # remove duplicate based on column
    updated_df = duplication_handler.remove_duplicates(updated_df, 'Mobile Phone')

    # populate campaign column
    updated_df = task_reactivation_subfile.assign_campaign(file_path, updated_df)

    # get date format
    date_format = task_reactivation_subfile.get_current_date()

    # rename file and save file
    new_file_name = task_reactivation_subfile.generate_file_name(file_path, date_format)
    task_reactivation_subfile.save_file(os.path.dirname(file_path), new_file_name, updated_df)

    # return these 4 variable to be used in main function
    return original_df, updated_df, new_file_name, excluded_df
    
# reactivation main function
def task_reactivation_main(folder_path):
    # add start time to record code runtime
    start_time = time.time()

    # Ignore warning 
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    logging.info('Processing Reactivation Files ...')

    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_reactivation\test_data\Apr'
    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\TM Schedule Files\TM Reactivation\2024\May'

    # generate sub folder path
    dl_folder = os.path.join(folder_path, 'DL')
    rl_folder = os.path.join(folder_path, 'RL')

    # create a list then append all file name in folder and sub folder
    file_list = []
    for folder in [dl_folder, rl_folder]:
        for subfolder in ['Reject', 'Cancel']:
            subfolder_path = os.path.join(folder, subfolder)

            for file in os.listdir(subfolder_path):
                file_list.append(file)
                
    # check if the prefix is already in file name in the list
    if any('TMRL' in file or 'TMDL' in file for file in file_list):
        logging.info('Files already been processed! Please check the folder') 
    else:
        # initiate list to get data
        processed_file_info = []
        deleted_list = []
        
        # iterate in folder and sub-folder
        for folder in [dl_folder, rl_folder]:
            for subfolder in ['Reject', 'Cancel']:
                subfolder_path = os.path.join(folder, subfolder)

                # include counter to add number to file name
                task_reactivation_subfile.reset_batch_counter()

                for file in os.listdir(subfolder_path):
                    # apply condition for updating file name purpose
                    if file.startswith('DL') and 'Reject' in file:
                        # build file path
                        file_path = os.path.join(subfolder_path, file)
                        # call process function
                        original_df, updated_df, new_file_name, excluded_df = process_files(file_path)

                    elif file.startswith('DL') and 'Cancel' in file:
                        file_path = os.path.join(subfolder_path, file)
                        original_df, updated_df, new_file_name, excluded_df = process_files(file_path)

                    elif file.startswith('RL') and 'Reject' in file:
                        file_path = os.path.join(subfolder_path, file)
                        original_df, updated_df, new_file_name, excluded_df = process_files(file_path)

                    elif file.startswith('RL') and 'Cancel' in file:
                        file_path = os.path.join(subfolder_path, file)
                        original_df, updated_df, new_file_name, excluded_df = process_files(file_path)

                    # check if the df is not empty then append to deleted_list
                    if not excluded_df.empty:
                        # add file name so that I know where the row belongs
                        excluded_df['File Name'] = new_file_name
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
            

    # print process status and analysis
    logging.info('Process completed!. Files has been saved in selected folder.')
    logging.info('Here is the file analysis for your reference.')
    # print a table to show list
    logging.info(tabulate(processed_file_info, headers="keys", tablefmt="grid")) 
    
    # get end time for runtime and print
    end_time = time.time()
    code_runtime = end_time - start_time
    logging.info('Processing Time: {:2f} seconds'.format(code_runtime))
