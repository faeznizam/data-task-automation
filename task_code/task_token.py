# import function from subfile
from .dependencies import token_subfile

# import dependency
import logging
import os


# main function
def task_token_main(folder_path):
    
    # using for loop to detect file based on file name and process accordingly
    if any('To Token' in file for file in os.listdir(folder_path)):
        logging.info('Files already been processed! Please check the folder')
    else:
        for file_name in os.listdir(folder_path):
            if 'ihvsmc' in file_name.lower():
                token_subfile.process_egfile(folder_path, file_name)
            elif 'fpvsmc' in file_name.lower():
                token_subfile.process_egfile(folder_path, file_name)
            elif 'eqvsmc' in file_name.lower():
                token_subfile.process_egfile(folder_path, file_name)
            elif 'new card' in file_name.lower():
                token_subfile.process_new_tokenfile(folder_path, file_name)

        # print process status and analysis
        logging.info('Process completed!. Files has been saved in selected folder.')
