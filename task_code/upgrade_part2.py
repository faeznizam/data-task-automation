# import from local module 
from .dependencies import process_upgrade, helper_deletion, helper_analyze

# import from library
import warnings
import logging
import os

def upgrade_part2_flow(folder_path):
   
    # Ignore warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    # check if the file with selected name has been process
    file_count_IH = sum('TMU_IH' in file for file in os.listdir(folder_path))
    file_count_SG = sum('TMU_SG' in file for file in os.listdir(folder_path))
    file_count_IP = sum('TMU_IP' in file for file in os.listdir(folder_path))

    print(f'IH : {file_count_IH}, IP : {file_count_IP}, SG : {file_count_SG}')
    
    if file_count_IP == 1:

        # initialize list to get data
        processed_file_info = []
        deleted_list = []
        
        # iterate file in folder
        for file in os.listdir(folder_path):

            if 'TMU' in file:
                # process file
                original_df, updated_df, excluded_df, new_file_name = process_upgrade.process_file(folder_path, file)
                
                # get deleted rows
                helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)
                
                # get row count
                helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)

        # create deleted list
        helper_deletion.create_deleted_list(deleted_list, folder_path)

        # create analysis table
        helper_analyze.analysis_table(processed_file_info)

        logging.info('Process Completed.')


                

               

      
        

    