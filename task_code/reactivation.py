# import from sub file
from .dependencies import process_reactivation, helper_analyze, helper_deletion

# import from module
import warnings
import logging
import os

def reactivation_subflow(subfolder_path, file, deleted_list, processed_file_info):
    file_path = os.path.join(subfolder_path, file)
    # call process function
    original_df, updated_df, excluded_df, new_file_name = process_reactivation.process_files(file_path, subfolder_path)

    # get deleted rows
    helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)

    # get row count
    helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)

    return deleted_list, processed_file_info

# reactivation main function
def reactivation_flow(folder_path):
  
    # Ignore warning 
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    # generate sub folder path
    dl_folder = os.path.join(folder_path, 'DL')
    rl_folder = os.path.join(folder_path, 'RL')

    # create a list then append all file name in folder and sub folder
    file_list = []
    for folder in [dl_folder, rl_folder]:
        for subfolder in ['Reject', 'Cancel']:
            subfolder_path = os.path.join(folder, subfolder)

            for file in os.listdir(subfolder_path):
                file_list.append(file)
                
    # check if the prefix is already in file name in the list
    if any('TMRL' in file or 'TMDL' in file for file in file_list):
        logging.info('Files already been processed! Please check the folder') 
    else:
        # initiate list to get data
        processed_file_info = []
        deleted_list = []
        
        # iterate in folder and sub-folder
        for folder in [dl_folder, rl_folder]:
            for subfolder in ['Reject', 'Cancel']:
                subfolder_path = os.path.join(folder, subfolder)

                # include counter to add number to file name
                process_reactivation.reset_batch_counter()

                for file in os.listdir(subfolder_path):
                    # apply condition for updating file name purpose
                    if file.startswith('DL') and 'Reject' in file:
                        deleted_list, processed_file_info = reactivation_subflow(subfolder_path, file, deleted_list, processed_file_info)
                        
                    elif file.startswith('DL') and 'Cancel' in file:
                        deleted_list, processed_file_info = reactivation_subflow(subfolder_path, file, deleted_list, processed_file_info)

                    elif file.startswith('RL') and 'Reject' in file:
                        deleted_list, processed_file_info = reactivation_subflow(subfolder_path, file, deleted_list, processed_file_info)

                    elif file.startswith('RL') and 'Cancel' in file:
                        deleted_list, processed_file_info = reactivation_subflow(subfolder_path, file, deleted_list, processed_file_info)

        # create deleted list
        helper_deletion.create_deleted_list(deleted_list, folder_path)

        # create analysis table
        helper_analyze.analysis_table(processed_file_info)

    logging.info('Process Completed.')
                    
               

    
    
    
