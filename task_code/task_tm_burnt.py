import pandas as pd
from datetime import datetime
import os
import warnings
from tabulate import tabulate

from script import clean_phone_number
from script import burnt_subfile
from script import remove_duplicate

def rename_file():
    # get current date
    current_date = datetime.now() # get current date
    date_format = current_date.strftime('%Y%m%d') # reformat date
    # create new file name
    new_file_name = 'TMBN_XB_UTS_' + str(date_format) + '.xlsx' # get new file name

    return new_file_name

def main():
    # remove warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_burnt\test_data'
    
    if not any('TMBN' in file for file in os.listdir(folder_path)):

        files = os.listdir(folder_path)

        # get file based on file name
        for file_name in files:
            
            # initialize list for saving file data
            processed_file_info = []

            if 'Burnt Report' in file_name:
                
                # get file path based on join folder path and file name
                file_path = os.path.join(folder_path, file_name)

                # read the excel file and set mailing zip and postal code to have string data type
                df = pd.read_excel(file_path, dtype={'Mailing Zip/Postal Code': str})

                # run function
                new_df = burnt_subfile.initalize_uts_file_format()
                new_df = burnt_subfile.copy_data(new_df, df)

                # clean phone number
                new_df = clean_phone_number.process_mobile_numbers(new_df)

                # delete duplicate based on mobile phone column
                new_df = remove_duplicate.remove_duplicates(new_df, 'Mobile Phone')

                # rename the file
                new_file_name = rename_file()

                # get new file name and join with folder path for output file
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
            print('Process completed')
            # print the list in table form
            print(tabulate(processed_file_info, headers="keys", tablefmt="grid"))   

    else:
        print('Files already been processed! Please check the folder') 

if __name__ == '__main__':
    main()