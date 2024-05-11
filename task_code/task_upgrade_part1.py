import pandas as pd
import os
import warnings
from tabulate import tabulate

def main():
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\task_simplify_project\test_data\Apr'

    dfs = []

    for file in os.listdir(folder_path):
        if 'SG' in file:
            file_path = os.path.join(folder_path, file)

            df = pd.read_excel(file_path)

            dfs.append(df)

    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df = merged_df[merged_df['Rollup Summary: Ttl # of Pledges'] == 1]
    merged_df = merged_df[(merged_df['Rollup Summary: Last Pledge Don Amt'] != merged_df['Donation Amount'])]
    selected_columns = ['Supporter ID', 'Rollup Summary: Last Pledge Don Amt', 'Donation Amount', 'Pledge ID', 'Serial Number']
    new_df = merged_df.loc[:, selected_columns ]

    new_file_name = 'To compare row SG.xlsx'
    new_file_path = os.path.join(folder_path, new_file_name)
    new_df.to_excel(new_file_path, index=False)

    print(f'{new_file_name} has been created!')
    print(f'Checking Blank Card Expiry in In House Files...')
    
    file_check = []

    for file in os.listdir(folder_path):
        if 'IH' in file:
            file_path = os.path.join(folder_path, file)

            df = pd.read_excel(file_path)

            card_expiry_blank = df['Card Expiry'].isna()
            card_expiry_blank_count = card_expiry_blank.sum()

            card_number_blank = df['Card Number (Partial Only)'].isna()
            card_number_blank_count = card_number_blank.sum()

            file_check.append({
                'File Name' : file,
                'Blank Card Number': card_number_blank_count ,
                'Blank Card Expiry': card_expiry_blank_count
            })

    print(tabulate(file_check, headers="keys", tablefmt="grid"))

    print('File has been checked and analyze!')



         


     






            

if __name__ == '__main__':
    main()


