import pandas as pd
import warnings
import os
import logging

from .dependencies import date_handler
from .dependencies import process_set_reject_burnt

def task_set_reject_burnt(folder_path):
    
    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_set_reject_burnt_status'
    
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')
    
    if not 'MCO To Burnt Report_to_upload' in os.listdir(folder_path) or not 'MCO To Rejected Report_to_upload' in os.listdir(folder_path):

        result_folder = os.path.join(folder_path, 'Results')
        os.makedirs(result_folder)

        logging.info('Result folder created.')

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            date = date_handler.current_date_format()

            if 'MCO To Burnt Report' in file:
                process_set_reject_burnt.process_burnt(file_path, folder_path, file, date)
                logging.info('Burnt file created.')
                
            elif 'MCO To Rejected Report' in file:
                process_set_reject_burnt.process_reject(file_path, folder_path, file, date)
                logging.info('Reject file created.')
        
        logging.info('Process complete.')

    else:
        logging.info('File has been processed. Check the folder!')
    
"""
if __name__ == '__main__':
    task_set_reject_burnt()

"""