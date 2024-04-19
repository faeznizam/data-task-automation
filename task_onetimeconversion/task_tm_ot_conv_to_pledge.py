# import module
import pandas as pd
from datetime import datetime
import os

# function
def process_mobile_numbers(df):
    # remove empty space and hyphens
    df['Mobile Phone'] = df['Mobile Phone'].str.replace(r'[ +\-]', '', regex=True)
    df['Mobile Phone'] = df['Mobile Phone'].apply(lambda x: reformat_mobile_number(x))
    
    return df

def reformat_mobile_number(x):

    if (x.startswith('01') and len(x) == 10) or (x.startswith('011') and len(x) == 11):
        return x[:3] + '-' + x[3:]
    else:
        return x

# main function 
def main(folder_path):
    
    files = os.listdir(folder_path)

    # check file availability using flag
    found_file = False

    for file_name in files:
        if 'TM One Time' in file_name:
            print(file_name)

            file_path = os.path.join(folder_path, file_name)
            df = pd.read_excel(file_path, dtype={'Post Code': str})

            df = process_mobile_numbers(df)

            # rename the file
            # get current date
            date = datetime.now()
            date_format = date.strftime('%Y%m%d')

            # new file name
            new_file_name = 'TMOC_UTS_' + str(date_format) + '.xlsx'
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # save file
            df.to_excel(new_file_path, index=False)
            print(f'File {new_file_name} been saved in the folder')

            # set flag to True if file found
            found_file = True

    if not found_file:
        print('File is not available. Check folder path for file.')

