# import module from folder
from .dependencies import process_burnt, helper_analyze, helper_deletion

# import dependency
import warnings
import logging
import os

def burnt_flow(folder_path):
    # Ignore warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_burnt'
    
    # check if files has been processed
    if any('TMBN' in file for file in os.listdir(folder_path)):
        print('Files already been processed! Please check the folder')
    else:
        # initialize list to get data
        processed_file_info = []
        deleted_list = []

        # iterate files in folder
        for file_name in os.listdir(folder_path):
            if 'Burnt Report' in file_name:

                #process file
                original_df, updated_df, excluded_df, new_file_name = process_burnt.process_file(folder_path, file_name)

                # get deleted rows
                helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)

                # get row count
                helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)
                
            # create deleted list
            helper_deletion.create_deleted_list(deleted_list, folder_path)

            # create analysis table
            helper_analyze.analysis_table(processed_file_info)

        logging.info('Process Completed.')


    

    
