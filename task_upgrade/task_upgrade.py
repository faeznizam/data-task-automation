import os
import pandas as pd
import warnings
from tabulate import tabulate

from script import uts_file_format
from script import copy_data_upgrade
from script import remove_duplicate
from script import clean_phone_number


def main():
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_upgrade\test_data\Mar'

    # check if the file with selected name has been process
    file_count = len(os.listdir(folder_path))
    if file_count == 9:

        # initialize list for saving file data
        processed_file_info = []

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            df = pd.read_excel(file_path)
            new_df = uts_file_format.initalize_uts_file_format()
            new_df = copy_data_upgrade.copy_data_upgrade(new_df, df)
            new_df = clean_phone_number.process_mobile_numbers(new_df)
            new_df = remove_duplicate.remove_duplicates(new_df, 'Mobile Phone')
            new_file_name = f'{file[:-12]}.xlsx'
            new_file_path = os.path.join(folder_path, new_file_name)
            new_df.to_excel(new_file_path, index=False)
            # get data into list
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

    else:
        print('Files already been processed! Please check the folder')

if __name__ == "__main__" :
    main()
        

    