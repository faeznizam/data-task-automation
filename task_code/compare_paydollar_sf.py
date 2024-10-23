import pandas as pd
import os
import warnings
import logging as log

"""
To create code for 2 part process.
1. To compare data between database file and transaction file
2. To filter data and compare between database file and transaction file

"""

# Configure logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def task_compare_paydollarsf(folder_path):
    # Ignore warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')
    
    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_compare_paydollar_sf\Entire Month'

    log.info('Process Files')
    for file in os.listdir(folder_path):
        # create donation column
        if 'Online OT' in file:
            file_path = os.path.join(folder_path, file)
            donation_df = pd.read_excel(file_path, dtype={'External Donation Reference Id': str})
            donation_df.rename(columns={
                'External Donation Reference Id' : 'External Reference Id',
                'Donation 18 Digit Id' : 'Id', 
                'Stage' : 'Old Stage'
            }, inplace=True)
            column_list1 = ['External Reference Id', 'Old Stage', 'Close Date', 'Type', 'Id']
            donation_column = donation_df[column_list1]
            

        elif 'Online Pledge Donation' in file:
            # create pledge column 
            file_path = os.path.join(folder_path, file)
            pledge_df = pd.read_excel(file_path, dtype={'External Pledge Reference Id' : str})
            pledge_df.rename(columns={
                'External Pledge Reference Id' : 'External Reference Id',
                'MCO Donation 18 digit Id' : 'Id',
                'Stage' : 'Old Stage'

            }, inplace=True)
            column_list2 = ['External Reference Id', 'Old Stage', 'Close Date', 'Type', 'Id']
            pledge_column = pledge_df[column_list2]
            

        elif 'order' in file:
            # create paydollar column 
            file_path = os.path.join(folder_path, file)
            paydollar_df = pd.read_excel(file_path, dtype={'Merchant Ref.' : str})

            drop_row_channel_type_DPL = paydollar_df['Channel Type'] == 'DPL'
            paydollar_df = paydollar_df[~drop_row_channel_type_DPL]

            selected_paydollar_column = ['Merchant Ref.', 'Transaction Date']
            paydollar_df = paydollar_df[selected_paydollar_column]

            paydollar_df = paydollar_df[paydollar_df['Merchant Ref.'].notna()]
            paydollar_df = paydollar_df.drop_duplicates()

            paydollar_df = paydollar_df.rename(columns={
                'Merchant Ref.' : 'External Reference Id', 
                'Transaction Date' : 'npe01__Payment_Date__c'
            })

        elif 'entire month' in file:
            file_path = os.path.join(folder_path, file)
            get_id_df = pd.read_excel(file_path, dtype={'npe01__Opportunity__r.npe03__Recurring_Donation__r.sescore__External_Pledge_Reference_Id__c' : str})

            delete_column_get_id_df_list = [
                '_','npe01__Opportunity__r','npe01__Opportunity__r.npe03__Recurring_Donation__r',
                'npe01__Opportunity__r.Name','Name','sescore__Payment_Response_Code__c','sescore__Response_Category__c','npe01__Payment_Date__c'
                ]
    
            get_id_df = get_id_df.drop(columns=delete_column_get_id_df_list)

            get_id_df = get_id_df.rename(columns={'npe01__Opportunity__r.npe03__Recurring_Donation__r.sescore__External_Pledge_Reference_Id__c' : 'External Reference Id'})
    

    

    

    log.info('Merge Pledge and OT file')
    # merge donation and pledge to form a list to be compared with paydollar column 
    pledge_ot_donation_combine = pd.concat([donation_column, pledge_column], ignore_index=True)
    pledge_ot_donation_combine = pledge_ot_donation_combine.dropna()
    pledge_ot_donation_combine.to_excel(os.path.join(folder_path, 'merged_df.xlsx'), index=False)

    log.info('Filter the file for Stage = Pledge and Close Lost')
    # to compare data with stage = pledge and Closed Lost with merchant ref from paydollar
    filter_condition = (pledge_ot_donation_combine['Old Stage'] == 'Pledged') | (pledge_ot_donation_combine['Old Stage'] == 'Closed Lost')
    filetered_pledge_ot_donation_combine = pledge_ot_donation_combine[filter_condition]

    log.info('Merge with Paydollar file')
    main_file = pd.merge(filetered_pledge_ot_donation_combine, paydollar_df, on='External Reference Id', how='left')

    log.info('Filter out empty transaction date row')
    filter_condition2 = main_file['npe01__Payment_Date__c'].notna()
    main_file = main_file[filter_condition2]

    log.info('Convert date time format to date')
    main_file['npe01__Payment_Date__c'] = pd.to_datetime(main_file['npe01__Payment_Date__c'], format='%d/%m/%Y %H:%M:%S')
    main_file['npe01__Payment_Date__c'] = main_file['npe01__Payment_Date__c'].dt.strftime('%Y-%m-%d')

    log.info('Add Response code column')
    main_file['sescore__Payment_Response_Code__c'] = 0

    main_file = main_file.drop(columns='Id')

    main_file = pd.merge(main_file, get_id_df, on='External Reference Id', how='left')

    log.info('Save to_set_close_won.xlsx')
    main_file.to_excel(os.path.join(folder_path, 'to_set_close_won.xlsx'), index=False)

    log.info('Compare data from Paydollar file and Pledge OT file')
    # compare the merge column and paydollar column 
    not_in_merge_df = paydollar_df[~paydollar_df['External Reference Id'].isin(pledge_ot_donation_combine['External Reference Id'])]
    not_in_merge_df = not_in_merge_df.dropna()

    # not in merge meaning there are transaction not created
    # so if the df is empty the print status, else create file
    if not_in_merge_df.empty:
        log.info('All transactions have been created!')
    else:
        not_in_merge_df = not_in_merge_df['External Reference Id']
        not_in_merge_df.to_excel(os.path.join(folder_path, 'transaction_not_created.xlsx'), index=False)
        log.info('A list of transaction not created has been created!')

    log.info('Process Complete')





#if __name__ == '__main__':
#    task_compare_paydollarsf()
