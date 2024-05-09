# import dependencies
import pandas as pd
import os
import warnings
from script import handle_duplication
from tabulate import tabulate

def main():

    # Ignore SettingWithCopyWarning
    pd.options.mode.chained_assignment = None

    # Ignore specific UserWarning from openpyxl.styles.stylesheet
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    print('Month 2 - 6 Process start!')

    # get folder path
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_month2_6\test_data'

    # initiate deleted list and process info
    deleted_list = []
    processed_file_info = []

    if not any('deleted_list' in file for file in os.listdir(folder_path)):
        
        print('Checking existing file...')
        print('No existing file detected. Creating the file...')

        # iterate over all the file in folder
        for file in os.listdir(folder_path):
            
            # build file path
            file_path = os.path.join(folder_path, file)

            # read file
            df = pd.read_excel(file_path)

            # fill in empty cell with empty string
            df = df.fillna('')
            # set up condition for filtering row to delete
            to_delete_row = ( ~df['Mailing Country'].str.lower().isin(['malaysia', 'brunei', 'brunei darussalam', 'singapore', '']) |
                        (df['Mailing Zip/Postal Code'] == "") | 
                        (df['Mailing Zip/Postal Code'] == '-')
                        )
            # get opposite condition 
            to_update_row = ~ to_delete_row
            # build both to update and to delete dataframe
            modified_df = df[to_update_row]
            df_to_delete = df[to_delete_row]

            # drop duplicate 
            modified_df = handle_duplication.remove_duplicates(modified_df, 'Mailing Street')

            # get new file name based on original file name
            new_file_name = f'{file[:-25]}.xlsx'
            # build file path
            new_file_path = os.path.join(folder_path, new_file_name)
            # save to excel 
            modified_df.to_excel(new_file_path, index=False)

            # set up condition to append to list when df is not empty
            if not df_to_delete.empty:
                # add file name to row
                df_to_delete['File Name'] = f'{file[:-25]}.xlsx'
                # append to list
                deleted_list.append(df_to_delete)

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

if __name__ == '__main__':
    main()