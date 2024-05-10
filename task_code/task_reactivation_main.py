# import from sub file
from dependencies import uts_file_format
from dependencies import copy_data_reactivation
from dependencies import task_reactivation_subfile
from dependencies import clean_phone_number
from dependencies import remove_duplicate

# import from module
import pandas as pd
import os
import warnings
from datetime import datetime
from tabulate import tabulate

# main
def process_files(file_path):
    df = task_reactivation_subfile.read_file(file_path)
    new_df = uts_file_format.initalize_uts_file_format()
    new_df = copy_data_reactivation.copy_data_reactivation(new_df, df)
    new_df = clean_phone_number.process_mobile_numbers(new_df) # boleh improve untuk buang no start selain 0
    new_df = remove_duplicate.remove_duplicates(new_df, 'Mobile Phone')
    new_df = task_reactivation_subfile.assign_campaign(file_path, new_df)
    date_format = task_reactivation_subfile.get_current_date()
    new_file_name = task_reactivation_subfile.generate_file_name(file_path, date_format)
    task_reactivation_subfile.save_file(os.path.dirname(file_path), new_file_name, new_df)

    return df, new_df, new_file_name
    
# reactivation
def main():
    # filter warning 
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    print('Processing Reactivation Files ...')

    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_reactivation\test_data\Apr'
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\TM Schedule Files\TM Reactivation\2024\May'

    dl_folder = os.path.join(folder_path, 'DL')
    rl_folder = os.path.join(folder_path, 'RL')

    file_list = []
    for folder in [dl_folder, rl_folder]:
        for subfolder in ['Reject', 'Cancel']:
            subfolder_path = os.path.join(folder, subfolder)

            for file in os.listdir(subfolder_path):
                file_list.append(file)
                
    
    if any('TMRL' in file or 'TMDL' in file for file in file_list):
        print('File already exist!. Check the folder')
    else:
        processed_file_info = []
        for folder in [dl_folder, rl_folder]:
            for subfolder in ['Reject', 'Cancel']:
                subfolder_path = os.path.join(folder, subfolder)

                task_reactivation_subfile.reset_batch_counter()

                for file in os.listdir(subfolder_path):
                    if file.startswith('DL') and 'Reject' in file:
                        file_path = os.path.join(subfolder_path, file)
                        df, new_df, new_file_name = process_files(file_path)
                    elif file.startswith('DL') and 'Cancel' in file:
                        file_path = os.path.join(subfolder_path, file)
                        df, new_df, new_file_name = process_files(file_path)
                    elif file.startswith('RL') and 'Reject' in file:
                        file_path = os.path.join(subfolder_path, file)
                        df, new_df, new_file_name = process_files(file_path)
                    elif file.startswith('RL') and 'Cancel' in file:
                        file_path = os.path.join(subfolder_path, file)
                        df, new_df, new_file_name = process_files(file_path)
                    

                    processed_file_info.append({
                        'File Name' : new_file_name, # get file name
                        'Before Clean' : len(df), # count before clean
                        'After Clean' : len(new_df), # count after clean
                        'Invalid Phone Number' : clean_phone_number.count_invalid_phone_number(new_df, 'Mobile Phone') # flag invalid mobile number
                    })
            

    # print completion status
    print('Process completed.')
    # print the list in table form
    print(tabulate(processed_file_info, headers="keys", tablefmt="grid"))

if __name__ == '__main__':
    main()
