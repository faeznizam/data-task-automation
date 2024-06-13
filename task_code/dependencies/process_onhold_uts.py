# import from local module
from .helper_mobile_phone import process_mobile_numbers, delete_condition
from .helper_duplication import remove_duplicates

# import from library
from datetime import datetime
import pandas as pd
import os

def rename_uts_file(file):

    current_date = datetime.now()
    date_format = current_date.strftime('%y%m%d')
    extract_file_number = file[-7:-5]
    
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
   updated_df = process_mobile_numbers(updated_df, 'Mobile Phone')

   # exclude invalid number rows and assign to new dataframe
   rows_to_exclude = delete_condition(updated_df, 'Mobile Phone')
   excluded_df = updated_df[rows_to_exclude]

   # use opposite condition to filter the wanted number
   rows_to_update = ~ rows_to_exclude
   updated_df = updated_df[rows_to_update]

   # delete duplicate based on phone number column
   updated_df = remove_duplicates(updated_df, 'Mobile Phone')
   
   # rename file and save file
   new_file_name = rename_uts_file(file)
   new_file_path = os.path.join(sub_folder_path, new_file_name)
   updated_df.to_excel(new_file_path, index=False)


   return original_df, updated_df, excluded_df, new_file_name




