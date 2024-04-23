# import module
import pandas as pd
from datetime import datetime
import os
import warnings
from tabulate import tabulate

from script import clean_phone_number
from script import remove_duplicate

def rename_file():
    # get current date
    current_date = datetime.now() # get current date
    date_format = current_date.strftime('%Y%m%d') # reformat date
    # create new file name
    new_file_name = 'TMOC_UTS_' + str(date_format) + '.xlsx' # get new file name

    return new_file_name

# main function 
def main():
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_onetimeconversion\test_data\Apr'
    
    if not any('TMBN' in file for file in os.listdir(folder_path)):

        files = os.listdir(folder_path)

        for file_name in files:

            # initialize list for saving file data
            processed_file_info = []


            if 'TM One Time' in file_name:
                print(file_name)

                file_path = os.path.join(folder_path, file_name)
                df = pd.read_excel(file_path, dtype={'Post Code': str})

                modified_df = df

                modified_df = clean_phone_number.process_mobile_numbers(modified_df)

                # rename the file
                new_file_name = rename_file()
                new_file_path = os.path.join(folder_path, new_file_name)
                
                # save file
                modified_df.to_excel(new_file_path, index=False)

                # get data into list
                processed_file_info.append({
                    'File Name' : new_file_name, # get file name
                    'Before Clean' : len(df), # count before clean
                    'After Clean' : len(modified_df), # count after clean
                    'Invalid Phone Number' : clean_phone_number.count_invalid_phone_number(modified_df, 'Mobile Phone') # flag invalid mobile number
                }) 


            # print completion status
            print('Process completed')
            # print the list in table form
            print(tabulate(processed_file_info, headers="keys", tablefmt="grid")) 

    else:
        print('Files already been processed! Please check the folder') 

    

if __name__ == '__main__':
    main()