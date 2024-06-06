from datetime import datetime
import pandas as pd
import os
import warnings
from tabulate import tabulate


from dependencies import mobile_phone_handler
from dependencies import duplication_handler

def rename_file(file):
    current_date = datetime.now() # get current date
    date_format = current_date.strftime('%Y%m%d') # reformat date

    return f'TM_{file[8:11]}{file[12:16]}_{file[16:18]}_OH{file[19:21]}_{date_format}.xlsx'

    

def main():
    # filter warning 
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_winbackonhold'

    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        file_count = len(os.listdir(subfolder_path))
        if file_count == 11:

            # initialize list for saving file data
            processed_file_info = []
            deleted_list = []

            for file in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file)

                original_df = pd.read_excel(file_path, dtype={'Post Code': str})

                updated_df = original_df

                updated_df = mobile_phone_handler.process_mobile_numbers(updated_df, 'Mobile Phone')

                # exclude invalid number rows and assign to new dataframe
                rows_to_exclude = mobile_phone_handler.delete_condition(updated_df, 'Mobile Phone')
                excluded_df = updated_df[rows_to_exclude]

                # use opposite condition to filter the wanted number
                rows_to_update = ~ rows_to_exclude
                updated_df = updated_df[rows_to_update]


                updated_df = duplication_handler.remove_duplicates(updated_df, 'Mobile Phone')


                new_file_name = rename_file(file)
                new_file_path = os.path.join(subfolder_path, new_file_name)

                updated_df.to_excel(new_file_path, index=False)

                # check if the df is not empty then append to deleted_list
                if not excluded_df.empty:
                    # add file name so that I know where the row belongs
                    excluded_df['File Name'] = new_file_name
                    deleted_list.append(excluded_df)


                processed_file_info.append({
                    'File Name' : new_file_name, # get file name
                    'Before Clean' : len(original_df), # count before clean
                    'After Clean' : len(updated_df), # count after clean
                })

            # combine all df that has been append to list and save the file in excel
            # empty list gave out False boolean
            if deleted_list:
                final_deleted_df = pd.concat(deleted_list, ignore_index=True)
                final_deleted_df.to_excel(os.path.join(folder_path, 'deleted_list.xlsx'), index=False)
            else:
                print('Deleted list was not created since there is no data!')# combine all df that has been append to list and save the file in excel

            # print process status and analysis
            print('Process completed!. Files has been saved in selected folder.')
            print('Here is the file analysis for your reference.')
            # print a table to show list
            print(tabulate(processed_file_info, headers="keys", tablefmt="grid")) 

             

        else:
            print('Files already been processed! Please check the folder')

if __name__ == '__main__':
    main()



