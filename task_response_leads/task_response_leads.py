import pandas as pd
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import warnings
from tabulate import tabulate

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
    new_file_name = f'MCO_UTS_RESPONSE_{date_format}_{previous_month_text}{extracted_name}'

    return new_file_name

def main():
    # remove warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_response_leads\test_data\Mar'

    # check if the file with selected name has been process
    if not any('MCO_UTS' in file for file in os.listdir(folder_path)):
        
        # initialize list for saving file data
        processed_file_info = []

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            # to preserve data with leading zero in these columns
            columns_with_leading_zero = ['Post Code', 'Donation Amount', 'Home Phone', 'Work Phone', 'Mobile Phone']
            # change dtype to str
            dtype_dict = {column : str for column in columns_with_leading_zero}

            # read file
            df = pd.read_excel(file_path, dtype=dtype_dict)

            # filter out column data = subscribe
            modified_df = df[df['Description'] != 'Subscribe']

            # applied rename file function
            new_file_name = rename_file(file)   

            # build file path for new file
            new_file_path = os.path.join(folder_path, new_file_name)

            # save file
            modified_df.to_excel(new_file_path, index=False)

            # get data into list
            processed_file_info.append({
                'File Name' : new_file_name, # get file name
                'Before Clean' : len(df), # count before clean
                'After Clean' : len(modified_df) # count after clean
                
            }) 

        # print completion status
        print('Process completed.')
        # print the list in table form
        print(tabulate(processed_file_info, headers="keys", tablefmt="grid"))

    else:
        print('Files already been processed! Please check the folder')  


if __name__ == '__main__':
    main()
