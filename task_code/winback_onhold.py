# import from local module
from .dependencies import process_winback_onhold, helper_deletion, helper_analyze

# import from library
import warnings
import logging
import os

def winback_onhold_flow(folder_path):
    # filter warning 
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_winbackonhold'

    # initialize list for saving file data
    processed_file_info = []
    deleted_list = []

    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        file_count = len(os.listdir(subfolder_path))
        if not file_count == 11:
            print('Files already been processed! Please check the folder')
        else:

            for file in os.listdir(subfolder_path):
                original_df, updated_df, excluded_df, new_file_name = process_winback_onhold.process_file(subfolder_path, file)

                # get deleted rows
                helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)
            
                # get row count
                helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)

    # create deleted list
    helper_deletion.create_deleted_list(deleted_list, folder_path)

    # create analysis table
    helper_analyze.analysis_table(processed_file_info)

    logging.info('\nProcess Completed.')


             

        
            



