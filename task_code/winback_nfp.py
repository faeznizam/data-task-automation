# import module from folder
from .dependencies import process_winback_nfp, helper_deletion, helper_analyze

# import dependencies
import warnings
import logging
import os




def winback_nfp_flow(folder_path):
    
    # ignore warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    # check if the file with selected name has been process
    if any('TMNFP' in file for file in os.listdir(folder_path)):
        logging.info('Files already been processed! Please check the folder')
    else:

        # initialize list for saving file data
        processed_file_info = []
        deleted_list = []

        # iterate over every file in the folder
        for file in os.listdir(folder_path):
            
            # process file
            original_df, updated_df, excluded_df, new_file_name = process_winback_nfp.process_file(folder_path, file)
            
            # get deleted rows
            helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)
            
            # get row count
            helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)

        # create deleted list
        helper_deletion.create_deleted_list(deleted_list, folder_path)

        # create analysis table
        helper_analyze.analysis_table(processed_file_info)

        logging.info('Process Completed.')

            
    

        


    