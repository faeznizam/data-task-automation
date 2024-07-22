# import from local module
from .dependencies import process_onetime_conversion, helper_deletion, helper_analyze

# import dependency
from tabulate import tabulate
import warnings
import logging
import os

def one_time_conversion_flow(folder_path):
    # Ignore warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    # check file
    if any('TMOC' in file for file in os.listdir(folder_path)):
        logging.info('Files already been processed! Please check the folder')
    else:
        # initialize list to get data
        deleted_list = []
        processed_file_info = []

        # process file
        for file_name in os.listdir(folder_path):
            if 'TM One Time' in file_name:
                
                # process file
                original_df, updated_df, excluded_df, new_file_name = process_onetime_conversion.process_file(folder_path, file_name)
                
                # get deleted rows
                helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)
                
                # get row count
                helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)

            # create deleted list
            helper_deletion.create_deleted_list(deleted_list, folder_path)

            # create analysis table
            helper_analyze.analysis_table(processed_file_info)

            logging.info(tabulate(process_onetime_conversion.count_by_campaign(updated_df), headers="keys", tablefmt="html"))

        logging.info('\nProcess Completed.')
