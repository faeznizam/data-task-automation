# import from local module
from .helper_mobile_phone import process_mobile_numbers, delete_condition
from .helper_duplication import remove_duplicates

# import from library
import pandas as pd
import os

def populate_campaign(df, file):
    if 'DS - CC 1 Month Prior to Card Expiry' in file:
        df['Campaign'] = '7015g000000h3rdAAA'
        df['Campaign Name'] = 'Card Pre Expiry Campaign'
        df['Description'] = 'Card Pre Expiry Campaign'
    
    elif 'DS - Debit Card Expiry Date' in file:
        df['Campaign'] = '7015g000000h3rdAAA'
        df['Campaign Name'] = 'Card Pre Expiry Campaign'
        df['Description'] = 'Card Pre Expiry Campaign'

    elif 'New Onhold HR Report - DS' in file:
        df['Campaign'] = '7015g000000pEcxAAE'
        df['Campaign Name'] = 'OnHold DS HR Month 1'
        df['Description'] = 'OnHold DS HR Month 1'
    
    return df

def process_ds(agency_folder):
    file_list = os.listdir(agency_folder)
   
    for file in file_list:
        if 'DS - CC 1 Month Prior to Card Expiry' in file:
            # process and return df
            file_path = os.path.join(agency_folder, file)
            credit_card_df = pd.read_excel(file_path, dtype={'Post Code': str})
            credit_card_df = populate_campaign(credit_card_df, file)
            
        elif 'DS - Debit Card Expiry Date' in file:
            # process and return df
            file_path = os.path.join(agency_folder, file)
            debit_card_df = pd.read_excel(file_path, dtype={'Post Code': str})
            debit_card_df = populate_campaign(debit_card_df, file)
            
        
    # concatenate file
    combine_df = pd.concat([credit_card_df,debit_card_df], ignore_index=True)

    updated_df = combine_df

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

    new_file_name = 'Card Pre Expiry Campaign.xlsx'
    new_file_path = os.path.join(agency_folder, new_file_name)
    updated_df.to_excel(new_file_path, index=False)

    return combine_df, updated_df, excluded_df, new_file_name


