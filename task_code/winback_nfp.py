# import module from folder
from .dependencies import process_winback_nfp, helper_deletion, helper_analyze

# import dependencies
from datetime import datetime
import warnings
import logging
import pandas as pd
import os


def winback_nfp_flow(folder_path):
    
    # ignore warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    # check if the file with selected name has been process
    if any('TMNFP' in file for file in os.listdir(folder_path)):
        logging.info('Files already been processed! Please check the folder')
    else:

        # initialize list for saving file data
        master_list = []
        processed_file_info = []
        deleted_list = []


        file_list = os.listdir(folder_path)

        # iterate over every file in the folder
        for file in file_list:
            
            # process file
            original_df, updated_df, excluded_df, new_file_name = process_winback_nfp.process_file(folder_path, file)
            
            # get deleted rows
            helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)
            
            # get row count
            helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)

            updated_df['Source File'] = file
            master_list.append(updated_df)

        # create deleted list
        helper_deletion.create_deleted_list(deleted_list, folder_path)

        # create analysis table
        helper_analyze.analysis_table(processed_file_info)

        # create master list
        current_date = datetime.now()
        date_format = current_date.strftime('%y%m%d') 
        master_data = pd.concat(master_list, ignore_index=True)
        master_data.to_excel(os.path.join(folder_path, f'master_list_{date_format}.xlsx'), index=False)

        logging.info('Process Completed.')

            
    

        


    