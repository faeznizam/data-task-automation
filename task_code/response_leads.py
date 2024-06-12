from .dependencies import process_response_leads, helper_analyze

# import dependencies
import warnings
import logging
import os



def response_leads_flow(folder_path):
    # ignore warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    # check if the file with selected name has been process
    if any('MCO_UTS' in file for file in os.listdir(folder_path)):
        logging.info('Files already been processed! Please check the folder')
    else:
        # initialize list for saving file data
        processed_file_info = []

        for file in os.listdir(folder_path):
            
            # process file
            original_df, updated_df, new_file_name = process_response_leads.process_file(folder_path, file)

            # get row count
            helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)

        # create analysis table
        helper_analyze.analysis_table(processed_file_info)

        logging.info('Process Completed.')

