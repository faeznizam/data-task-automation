import pandas as pd
from datetime import datetime
import os


def get_deleted_info(excluded_df, deleted_list, new_file_name):

    # check if the df is not empty then append to deleted_list
    if not excluded_df.empty:
        # add file name so that I know where the row belongs
        excluded_df['File Name'] = new_file_name
        deleted_list.append(excluded_df)
        

def create_deleted_list(deleted_list, folder_path):
    current_date = datetime.now()
    date_format = current_date.strftime('%y%m%d') 

    # empty list gave out False boolean
    if deleted_list:
        final_deleted_df = pd.concat(deleted_list, ignore_index=True)
        final_deleted_df.to_excel(os.path.join(folder_path, f'deleted_list_{date_format}.xlsx'), index=False)
    else:
        print('No deleted list created.')

def create_deleted_list_startek(deleted_list, folder_path):
    # empty list gave out False boolean
    if deleted_list:
        final_deleted_df = pd.concat(deleted_list, ignore_index=True)
        final_deleted_df.to_excel(os.path.join(folder_path, 'startek_deleted_list.xlsx'), index=False)
    else:
        print('No deleted list created.')