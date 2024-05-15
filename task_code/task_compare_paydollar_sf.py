import pandas as pd
import os

"""
To create code for 2 part process.
1. To compare data between 2 file. 
2. To filter data and compare between 2 file. 

"""

def main():
    # get folder path
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_compare_paydollar_sf'

    for file in os.listdir(folder_path):
        # create donation column
        if 'Online OT' in file:
            file_path = os.path.join(folder_path, file)
            donation_df = pd.read_excel(file_path, dtype={'External Donation Reference Id': str})
            donation_df.rename(columns={
                'External Donation Reference Id' : 'External Reference Id'
            }, inplace=True)
            column_list1 = ['External Reference Id', 'Stage', 'Close Date', 'Type']
            donation_column = donation_df[column_list1]
            

        elif 'Online Pledge Donation' in file:
            # create pledge column 
            file_path = os.path.join(folder_path, file)
            pledge_df = pd.read_excel(file_path, dtype={'External Pledge Reference Id' : str})
            pledge_df.rename(columns={
                'External Pledge Reference Id' : 'External Reference Id'
            }, inplace=True)
            column_list2 = ['External Reference Id', 'Stage', 'Close Date', 'Type']
            pledge_column = pledge_df[column_list2]
            

        elif 'order' in file:
            # create paydollar column 
            file_path = os.path.join(folder_path, file)
            paydollar_df = pd.read_excel(file_path, dtype={'Merchant Ref.' : str})
            drop_row = paydollar_df['Channel Type'] == 'DPL'
            filtered_paydollar_df = paydollar_df[~drop_row]
            paydollar_column = filtered_paydollar_df['Merchant Ref.']
            dedup_paydollar_column = paydollar_column.drop_duplicates()

            
    # merge donation and pledge to form a list to be compared with paydollar column 
    merge_df = pd.concat([donation_column, pledge_column], ignore_index=True)
    merge_df = merge_df.dropna()
    merge_df.to_excel(os.path.join(folder_path, 'merged_df.xlsx'), index=False)
    
    # to compare data data with stage = pledge with merchant ref from paydollar
    condition = merge_df['Stage'] == 'Pledge'
    merge_df_pledge = merge_df[condition]

    if merge_df_pledge.empty:
        print('No data with Pledge Stage!')
    else:
        # compare
        condition2 = paydollar_column.isin(merge_df_pledge['External Reference Id'])
        to_set_closewon_list = paydollar_column[condition2]

        print('Creating file with Pledge State')
        to_set_closewon_list.to_excel(os.path.join(folder_path, 'to_set_closewon.xlsx'), index=False)

    # compare the merge column and paydollar column 
    not_in_merge_df = dedup_paydollar_column[~dedup_paydollar_column.isin(merge_df['External Reference Id'])]
    not_in_merge_df = not_in_merge_df.dropna()

    # not in merge meaning there are transaction not created
    # so if the df is empty the print status else create file
    if not_in_merge_df.empty:
        print('All transactions have been created!')
    else:
        not_in_merge_df.to_excel(os.path.join(folder_path, 'transaction_not_created.xlsx'), index=False)
        print('A list of transaction not created has been created!')



    


    

  



        
    
    




    

if __name__ == '__main__':
    main()