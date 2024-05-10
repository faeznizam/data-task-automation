import pandas as pd
import os
import warnings
from tabulate import tabulate

from dependencies import clean_phone_number
from dependencies import remove_duplicate

def rename_file(file):
    return f'{file[:-12]}.xlsx'

def main():
    # filter warning 
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_winbackonhold\test_data\Apr'

    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        file_count = len(os.listdir(subfolder_path))
        if file_count == 11:

            # initialize list for saving file data
            processed_file_info = []

            for file in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file)

                df = pd.read_excel(file_path, dtype={'Post Code': str})

                modified_df = df
                modified_df = clean_phone_number.process_mobile_numbers(modified_df)
                modified_df = remove_duplicate.remove_duplicates(modified_df, 'Mobile Phone')
                new_file_name = rename_file(file)
                new_file_path = os.path.join(subfolder_path, new_file_name)
                modified_df.to_excel(new_file_path, index=False)
                processed_file_info.append({
                    'File Name' : new_file_name, # get file name
                    'Before Clean' : len(df), # count before clean
                    'After Clean' : len(modified_df), # count after clean
                    'Invalid Phone Number' : clean_phone_number.count_invalid_phone_number(modified_df, 'Mobile Phone') # flag invalid mobile number
                })
            # print completion status
            print('Process completed.')
            # print the list in table form
            print(tabulate(processed_file_info, headers="keys", tablefmt="grid")) 

        else:
            print('Files already been processed! Please check the folder')

if __name__ == '__main__':
    main()



