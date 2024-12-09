# local dependencies for one time conversion task
from .dependencies import process_onetime_conversion, helper_deletion, helper_analyze

from tabulate import tabulate # format data into tabulate form for display
import warnings # to handle warning
import logging # log message for monitoring
import os # to interact with file system

def one_time_conversion_flow(folder_path):
    """
    This is main function for one time conversion task. 

    Parameter:
    folder path containing file to process
    
    It performs the following steps:
    1. Check if the file has been processed by checking the prefix. if yes then it will stop the process
        and prompt a message. 
    2. Initiate list to store data for deleted list and file info.
    3. Iterate over all the files in the folder and process only file match the condition set.
    4. For each file processed, extract excluded listing, row count and file name. 
    5. Append the listing, count, and file name into the list created. 
    6. Save excluded list in separate file.
    7. Tabulate the row count and file name.
    8. Display tabulated data at UI.

    Output:
    - one processed file 
    - a file containing excluded list

    """

    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    

    # list files in the folder
    files_in_directory = os.listdir(folder_path)

    if any('TMOC' in file for file in files_in_directory):
        logging.info('Files already been processed! Please check the folder')
        return
    
    deleted_list = []
    processed_file_info = []

    files_to_process = [file for file in files_in_directory if 'TM One Time' in file]

    for file_name in files_to_process:
        original_df, updated_df, excluded_df, new_file_name = process_onetime_conversion.process_file(folder_path, file_name)
        helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)
        helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)

    helper_deletion.create_deleted_list(deleted_list, folder_path)
    helper_analyze.analysis_table(processed_file_info)

    logging.info(tabulate(process_onetime_conversion.calculate_count_by_campaign(updated_df), headers="keys", tablefmt="html"))
    logging.info('\nProcess Completed.')
