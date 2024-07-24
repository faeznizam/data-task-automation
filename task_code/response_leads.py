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
        deceased_list = []
        do_not_call_list = []


        for file in os.listdir(folder_path):
            
            # process file
            original_df, updated_df, new_file_name, deceased_df, do_not_call_df = process_response_leads.process_file(folder_path, file)

            # get decease and donotcall data
            process_response_leads.get_decease_and_donotcall_data(deceased_df,do_not_call_df, deceased_list, do_not_call_list, new_file_name)

            # get row count
            helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)

        # create analysis table
        helper_analyze.analysis_table(processed_file_info)

        # create decease list and donotcall list
        process_response_leads.create_decease_and_donotcall_list(folder_path, deceased_list, do_not_call_list)

        logging.info('Process Completed.')

