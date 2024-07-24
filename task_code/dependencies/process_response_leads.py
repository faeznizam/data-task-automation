from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd
import os

def rename_file(file):
    # get extracted name from original file name
    extracted_name = file[19:]

    # get current date and reformat them
    current_date = datetime.now()
    date_format = current_date.strftime('%y%m%d')
    
    # to get previous month text in 3 letter form
    previous_month = current_date - relativedelta(months=1)
    previous_month_text = previous_month.strftime('%b')

    # rename the file
    return f'MCO_UTS_RESPONSE_{date_format}_{previous_month_text}{extracted_name}'

    
def process_file(folder_path, file):
    
    
    file_path = os.path.join(folder_path, file)

    # to preserve data with leading zero in these columns
    columns_with_leading_zero = ['Post Code', 'Donation Amount', 'Home Phone', 'Work Phone', 'Mobile Phone']
    # change dtype to str
    dtype_dict = {column : str for column in columns_with_leading_zero}

    # read file
    original_df = pd.read_excel(file_path, dtype=dtype_dict)

    # filter out column data = subscribe
    updated_df = original_df[original_df['Description'] != 'Subscribe']

    # applied rename file function
    new_file_name = rename_file(file)   

    # build file path for new file
    new_file_path = os.path.join(folder_path, new_file_name)

    # save file
    updated_df.to_excel(new_file_path, index=False)

    # create list for decease and do not call
    deceased_df = original_df[original_df['Description'] == 'Deceased']

    # drop all column except Donor Id
    column_to_keep = 'Donor Id'
    deceased_df = deceased_df[[column_to_keep]]

    do_not_call_df = original_df[original_df['Description'] == 'Never Call / Do Not Contact']

    # drop all column except Donor Id
    column_to_keep2 = 'Donor Id'
    do_not_call_df = do_not_call_df[[column_to_keep2]]

    return original_df, updated_df, new_file_name, deceased_df, do_not_call_df

def get_decease_and_donotcall_data(deceased_df, do_not_call_df, deceased_list, do_not_call_list,new_file_name):
    
    if not deceased_df.empty:
        deceased_df.rename(columns={'Donor Id' : 'sescore__Supporter_Id__c'})
        deceased_df['npsp__Deceased__c'] = 'TRUE'
        deceased_df['npsp__Do_Not_Contact__c'] ='TRUE'
        deceased_df['file'] = new_file_name
        deceased_list.append(deceased_df)

    if not do_not_call_df.empty:
        do_not_call_df.rename(columns={'Donor Id' : 'sescore__Supporter_Id__c'})
        do_not_call_df['sescore__Phone_Consent__c'] = 'FALSE'
        do_not_call_df['DoNotCall'] = 'TRUE'
        do_not_call_df['file'] = new_file_name
        do_not_call_list.append(do_not_call_df)

def create_decease_and_donotcall_list(folder_path, deceased_list, do_not_call_list):
    if deceased_list:
        final_deceased_df = pd.concat(deceased_list, ignore_index=True)
        final_deceased_df.to_csv(os.path.join(folder_path, 'decease_file.csv'), index=False)

    if do_not_call_list:
        final_donotcall_df = pd.concat(do_not_call_list, ignore_index=True)
        final_donotcall_df.to_csv(os.path.join(folder_path, 'donot_call_file.csv'), index=False)



    