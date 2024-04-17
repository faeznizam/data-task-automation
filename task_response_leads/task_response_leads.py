import pandas as pd
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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

def main(folder_path):

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        # to preserve data with leading zero in these columns
        columns_with_leading_zero = ['Post Code', 'Donation Amount', 'Home Phone', 'Work Phone', 'Mobile Phone']
        # change dtype to str
        dtype_dict = {column : str for column in columns_with_leading_zero}

        # read file
        df = pd.read_excel(file_path, dtype=dtype_dict)

        # filter out column data = subscribe
        updated_df = df[df['Description'] != 'Subscribe']

        # applied rename file function
        new_file_name = rename_file(file)   

        # build file path for new file
        new_file_path = os.path.join(folder_path, new_file_name)

        # save file
        updated_df.to_excel(new_file_path, index=False)

        # print for visibility
        print(f'Renamed {file} to {new_file_name} !. File Length: Original/New - {len(df)}/{len(updated_df)}')


if __name__ == '__main__':
    main()
