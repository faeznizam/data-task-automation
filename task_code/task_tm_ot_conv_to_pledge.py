# import module
import pandas as pd
from datetime import datetime
import os
import warnings
from tabulate import tabulate
import time
from dependencies import clean_phone_number
from dependencies import remove_duplicate

def rename_file():
    # get current date
    current_date = datetime.now() # get current date
    date_format = current_date.strftime('%Y%m%d') # reformat date
    # create new file name
    new_file_name = 'TMOC_UTS_' + str(date_format) + '.xlsx' # get new file name

    return new_file_name

# main function 
def main():
    # get start time
    start_time = time.time()
    # ignore warning
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')
    warnings.filterwarnings("ignore", category=FutureWarning)

    print('Processing One Time Conversion To Pledge file...')

    # get folder path
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_onetimeconversion'
    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\TM Schedule Files\TM One time conversion\2024\May'

    # check existing file
    if not any('TMOC' in file for file in os.listdir(folder_path)):
        
        print('Checking existing file...')
        print('No existing file detected. Creating the file...')

        # initialize list for saving file data
        processed_file_info = []
        deleted_list = []

        # iterate all file in folder
        for file_name in os.listdir(folder_path):

            if 'TM One Time' in file_name:
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_excel(file_path, dtype={'Post Code': str})

                modified_df = df

                modified_df = clean_phone_number.process_mobile_numbers(modified_df)

                # get condition to delete and build to delete list
                to_delete_row = clean_phone_number.delete_condition(modified_df, 'Mobile Phone')
                to_delete_df = modified_df[to_delete_row]

                # get opposite condition and build the final list
                to_update_row = ~ to_delete_row
                modified_df = modified_df[to_update_row]

                # remove duplicate
                modified_df = remove_duplicate.remove_duplicates(modified_df, 'Mobile Phone')

                # rename the file
                new_file_name = rename_file()
                new_file_path = os.path.join(folder_path, new_file_name)
                
                # save file
                modified_df.to_excel(new_file_path, index=False)

                # set up condition to append to list when df is not empty
                if not to_delete_df.empty:
                    # add file name to row
                    to_delete_df['File Name'] = new_file_name
                    # append to list
                    deleted_list.append(to_delete_df)

                # get data into list
                processed_file_info.append({
                    'File Name' : new_file_name, # get file name
                    'Before Clean' : len(df), # count before clean
                    'After Clean' : len(modified_df), # count after clean
                    
                }) 

            # combine all df in the list
            final_deleted_df = pd.concat(deleted_list, ignore_index=True)
            # save to excel
            final_deleted_df.to_excel(os.path.join(folder_path, 'deleted_list.xlsx'), index=False)
            
            # print completion status
            print('Process completed!')
            print('Files has been saved in selected folder. ')
            # print the list in table form
            print('Here is the file analysis for your reference.')
            print(tabulate(processed_file_info, headers="keys", tablefmt="grid")) 

    else:
        print('Files already been processed! Please check the folder') 

    # get running end time and calculate total runtime
    end_time = time.time()
    code_runtime = end_time - start_time
    print('Processing Time: {:2f} seconds'.format(code_runtime))

if __name__ == '__main__':
    main()