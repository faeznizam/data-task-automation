# import function from subfile
from .dependencies import token_subfile

# import dependency
import logging
import os
import time

# main function
def task_token_main(folder_path):
    # add start time to record code runtime
    start_time = time.time()

    logging.info('Processing Token file...')
    
    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\TM Schedule Files\Tokenization\2024\May\09'

    # using for loop to detect file based on file name and process accordingly
    if not any('To Token' in file for file in os.listdir(folder_path)):

        for file_name in os.listdir(folder_path):
            if 'vsmc' in file_name.lower():
                token_subfile.process_egfile(folder_path, file_name)
            elif 'new card' in file_name.lower():
                token_subfile.process_new_tokenfile(folder_path, file_name)

        # print process status and analysis
        logging.info('Process completed!. Files has been saved in selected folder.')
            
    else:
        logging.info('Files already been processed! Please check the folder')
        

    # get end time for runtime and print
    end_time = time.time()
    code_runtime = end_time - start_time
    logging.info('Processing Time: {:2f} seconds'.format(code_runtime))