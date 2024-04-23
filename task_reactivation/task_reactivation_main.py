# import from sub file
from .script import uts_file_format
from .script import copy_data_reactivation
from .script import task_reactivation
from .script import clean_phone_number

# import from module
import pandas as pd
import os
import warnings
from datetime import datetime

# main
def process_files(file_path):
    df = task_reactivation.read_file(file_path)
    new_df = uts_file_format.initalize_uts_file_format()
    new_df = copy_data_reactivation.copy_data_reactivation(new_df, df)
    new_df = clean_phone_number.process_mobile_numbers(new_df) # boleh improve untuk buang no start selain 0
    new_df = task_reactivation.remove_duplicates(new_df)
    new_df = task_reactivation.assign_campaign(file_path, new_df)
    date_format = task_reactivation.get_current_date()
    new_file_name = task_reactivation.generate_file_name(file_path, date_format)
    task_reactivation.save_file(os.path.dirname(file_path), new_file_name, new_df)
    
# reactivation
def main(folder_path):
    # filter warning 
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    dl_folder = os.path.join(folder_path, 'DL')
    rl_folder = os.path.join(folder_path, 'RL')

    for folder in [dl_folder, rl_folder]:
        for subfolder in ['Reject', 'Cancel']:
            subfolder_path = os.path.join(folder, subfolder)

            task_reactivation.reset_batch_counter()

            for file in os.listdir(subfolder_path):
                if file.startswith('DL') and 'Reject' in file:
                    file_path = os.path.join(subfolder_path, file)
                    print(file_path)
                    process_files(file_path)
                elif file.startswith('DL') and 'Cancel' in file:
                    file_path = os.path.join(subfolder_path, file)
                    print(file_path)
                    process_files(file_path)
                elif file.startswith('RL') and 'Reject' in file:
                    file_path = os.path.join(subfolder_path, file)
                    print(file_path)
                    process_files(file_path)
                elif file.startswith('RL') and 'Cancel' in file:
                    file_path = os.path.join(subfolder_path, file)
                    print(file_path)
                    process_files(file_path)
                else:
                    pass

    print('Reactivation file process completed! Double check the files before sent!')
    



