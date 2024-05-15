import pandas as pd
import os
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

def main():

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_compare_paydollar_sf'

    for file in os.listdir(folder_path):
        if 'Online OT' in file:
            file_path = os.path.join(folder_path, file)


            df = pd.read_excel(file_path, dtype={'External Donation Reference Id': str})

            df1 = df['External Donation Reference Id']

            print('printing df1')
            print(df1)


        
            
        elif 'Online Pledge Donation' in file:

            file_path = os.path.join(folder_path, file)

            df = pd.read_excel(file_path, dtype={'External Pledge Reference Id' : str})

            df2 = df['External Pledge Reference Id']


            print('printing df2')
            print(df2)

        
            
        elif 'order' in file:
            # CHANNEL TYPE BUANG DPL

            file_path = os.path.join(folder_path, file)


            df = pd.read_excel(file_path, dtype={'Merchant Ref.' : str})


            df3 = df['Merchant Ref.']

            

            print(df3)


         

    merge_df = pd.concat([df1,df2], ignore_index=True)

    merge_df = merge_df.dropna()

    merge_df.to_excel(os.path.join(folder_path, 'merged_df.xlsx'), index=False)

    print(merge_df)

    not_in_merge_df = df3[~df3.isin(merge_df)]
    not_in_merge_df.to_excel(os.path.join(folder_path, 'not_in_merge_df.xlsx'), index=False)

# import dependency

# read file

# rename file, read file, get merchant ref column

# read both file, get both column 

# combine the column

# compare both column to see missing row

# if there is row missing, print id, if not print no row

# from compared both column, get stage = pledge. 

# if there is row match, save the file.

# if not print no row match with stage = pledge. 

# end
        
    
    




    

if __name__ == '__main__':
    main()