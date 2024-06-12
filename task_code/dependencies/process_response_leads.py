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

    return original_df, updated_df, new_file_name



    