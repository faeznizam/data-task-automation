# import module from folder
from .dependencies import process_month_2_to_6, helper_analyze, helper_deletion

# import dependencies
import pandas as pd
import os
import warnings
import logging

def month_2_to_6_flow(folder_path):
    # Ignore SettingWithCopyWarning and openpyxl.styles.stylesheet
    pd.options.mode.chained_assignment = None
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    

    # check if files already been processed
    if any('deleted_list' in file for file in os.listdir(folder_path)):
        logging.info('Files already been processed! Please check the folder') 
    else:
        # initiate deleted list and process info
        processed_file_info = []
        deleted_list = []

        # iterate over all the file in folder
        for file in os.listdir(folder_path):

            #process file
            original_df, updated_df, excluded_df, new_file_name = process_month_2_to_6.process_file(folder_path, file)
            
            # get deleted rows
            helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)

            # get row count
            helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)
            
        # create deleted list
        helper_deletion.create_deleted_list(deleted_list, folder_path)

        # create analysis table
        helper_analyze.analysis_table(processed_file_info)

        logging.info('Process Completed.')

    

