import pandas as pd
import logging as log
import os

# Configure logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def import_donation_notin_sf_main(folder_path):

    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_import_donation_notin_sf'

    order_df_filename = 'order.xlsx'
    recurring_df_filename = 'recurring donation in sf.xlsx'

    order_df_filepath = os.path.join(folder_path, order_df_filename)
    recurring_df_filepath = os.path.join(folder_path, recurring_df_filename)

    log.info('Read files')
    order_df = pd.read_excel(order_df_filepath, dtype={'Merchant Ref.' : str})
    recurring_df = pd.read_excel(recurring_df_filepath, dtype={'npe01__Opportunity__r.npe03__Recurring_Donation__r.sescore__External_Pledge_Reference_Id__c' : str})

    log.info('Filter row for order file')
    filter_condition = order_df['Channel Type'] == 'SCH'
    filtered_order_df = order_df[filter_condition]

    log.info('Delete columns')
    delete_column_order_df_list = [
        'System Ref.','Payment Mtd.','Card/Account','Exp Month','Exp Year','App Code','Bank Ref.','Holder Name',
        'Currency','Original Amount','Amount','Status','Card Issuing Bank (System)','Card Type','Remark','Channel Type'
        ]
    
    filtered_order_df = filtered_order_df.drop(columns=delete_column_order_df_list)

    delete_column_recurring_df_list = [
        '_','npe01__Opportunity__r','npe01__Opportunity__r.npe03__Recurring_Donation__r',
        'npe01__Opportunity__r.Name','Name','sescore__Payment_Response_Code__c','sescore__Response_Category__c','npe01__Payment_Date__c'
        ]
    
    recurring_df = recurring_df.drop(columns=delete_column_recurring_df_list)

    log.info('Rename columns')
    filtered_order_df = filtered_order_df.rename(columns={'Transaction Date' : 'npe01__Payment_Date__c', 'Merchant Ref.' : '__sescore__External_Pledge_Reference_Id__c'})
    recurring_df = recurring_df.rename(columns={'npe01__Opportunity__r.npe03__Recurring_Donation__r.sescore__External_Pledge_Reference_Id__c' : '__sescore__External_Pledge_Reference_Id__c'})

    log.info('Add new column and assign value')
    filtered_order_df['sescore__Payment_Response_Code__c'] = 0


    log.info('Convert date time format to date')
    filtered_order_df['npe01__Payment_Date__c'] = pd.to_datetime(filtered_order_df['npe01__Payment_Date__c'], format='%d/%m/%Y %H:%M:%S')
    filtered_order_df['npe01__Payment_Date__c'] = filtered_order_df['npe01__Payment_Date__c'].dt.strftime('%Y-%m-%d')

    log.info('Merge file')
    merge_df = pd.merge(filtered_order_df, recurring_df, on='__sescore__External_Pledge_Reference_Id__c', how='left')

    log.info('Rearrange column')
    new_column_format = ['__sescore__External_Pledge_Reference_Id__c', 'npe01__Payment_Date__c','sescore__Payment_Response_Code__c', 'Id']
    merge_df = merge_df[new_column_format]

    log.info('Review Result')
    missing_id_count = merge_df['Id'].isna().sum()

    if missing_id_count != 0:
        log.info(f'There are {missing_id_count} missing Id in the table!')
    else:
        log.info('Everything is good to go!')
        
    log.info('Saving file')
    merge_df.to_excel(os.path.join(folder_path, 'to export.xlsx'), index=False)

    log.info('Process complete!')

"""
if __name__ == '__main__':
    import_donation_notin_sf_main()

"""

    
