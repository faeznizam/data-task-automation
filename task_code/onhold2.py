# import from local module
from dependencies import helper_mobile_phone
from dependencies import helper_duplication
from dependencies import helper_analyze, helper_deletion

# import module 
from datetime import datetime
import pandas as pd
import os
import re

def create_new_filename(file):

    current_date = datetime.now()
    date_format = current_date.strftime('%y%m%d') 
    
    # Extract M1 to M6 using regex
    match = re.search(r'\bM[1-6]\b', file)
    if match:
        extract_file_number = match.group()
    else:
        extract_file_number = 'XX'  # fallback if pattern not found
    

    if 'HR' in file:
        return f'TM_UTS_HR_OH{extract_file_number}_{date_format}.xlsx'
    elif 'SR' in file:
        return f'TM_UTS_SR_OH{extract_file_number}_{date_format}.xlsx'
    else:
        pass

def populate_campaign(df, file):
    if 'HR' in file:
        df['Campaign'] = '7015g000000pEcvAAE'
        df['Campaign Name'] = 'OnHold UTS HR'
        df['Description'] = 'OnHold UTS HR'

    elif 'SR' in file:
        df['Campaign'] = '7015g000000pEqfAAE'
        df['Campaign Name'] = 'OnHold UTS SR'
        df['Description'] = 'OnHold UTS SR'
    
    return df

def process_uts(sub_folder_path, file):
   
    file_path = os.path.join(sub_folder_path, file)

    # read file and copy to new variable
    original_df = pd.read_excel(file_path, dtype={'Post Code' : str})
    updated_df = original_df

    # populate campaign
    updated_df = populate_campaign(updated_df, file)

    # clean phone number column
    updated_df = helper_mobile_phone.process_mobile_numbers(updated_df, 'Mobile Phone')

    # exclude invalid number rows and assign to new dataframe
    rows_to_exclude = helper_mobile_phone.delete_condition(updated_df, 'Mobile Phone')
    excluded_df = updated_df[rows_to_exclude]

    # use opposite condition to filter the wanted number
    rows_to_update = ~ rows_to_exclude
    updated_df = updated_df[rows_to_update]

    # delete duplicate based on phone number column
    updated_df = helper_duplication.remove_duplicates(updated_df, 'Mobile Phone')

    # remove last donation date
    column_to_remove = 'Last Donation Date'

    if column_to_remove in updated_df.columns:
        updated_df.drop(column_to_remove, axis=1, inplace=True)

    # remove data in unique id column
    updated_df['Unique Id'] = ''

    # rename file and save file
    new_file_name = create_new_filename(file)
    new_file_path = os.path.join(sub_folder_path, new_file_name)
    updated_df.to_excel(new_file_path, index=False)


    return original_df, updated_df, excluded_df, new_file_name



def main():
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Recurring Task\On Hold\2025\May\Test'

    # initiate list
    master_list = []
    processed_file_info = []
    deleted_list = []

    file_list = os.listdir(folder_path)

    for file in file_list:
        if 'New Onhold' in file:

            # process file
            original_df, updated_df, excluded_df, new_file_name = process_uts(folder_path, file)
            
            # get deleted rows
            helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)
            
            # get row count
            helper_analyze.get_row_count_and_amount(original_df, updated_df, new_file_name, processed_file_info)

            updated_df['Source File'] = file
            master_list.append(updated_df)

    # create deleted list
    helper_deletion.create_deleted_list(deleted_list, folder_path)

    # create analysis table
    helper_analyze.analysis_table(processed_file_info)

    # create master list
    current_date = datetime.now()
    date_format = current_date.strftime('%y%m%d') 
    master_data = pd.concat(master_list, ignore_index=True)
    master_data.to_excel(os.path.join(folder_path, f'master_list_{date_format}.xlsx'), index=False)

    print('Process Complete')
    

if __name__ == "__main__":
    main()