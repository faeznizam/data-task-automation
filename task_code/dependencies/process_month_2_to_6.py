# import module from folder
from .duplication_handler import remove_duplicates

# import dependencies
import pandas as pd
import os


def process_file(folder_path, file):
    file_path = os.path.join(folder_path, file)

    # read file
    original_df = pd.read_excel(file_path)
    updated_df = original_df

    # fill in empty cell with empty string
    updated_df = updated_df.fillna('')

    # set up condition for filtering row to delete and assign new dataframe
    rows_to_exclude = ( ~updated_df['Mailing Country'].str.lower().isin(['malaysia', 'brunei', 'brunei darussalam', 'singapore', '']) |
                (updated_df['Mailing Zip/Postal Code'] == "") | 
                (updated_df['Mailing Zip/Postal Code'] == '-')
                )
    excluded_df = updated_df[rows_to_exclude]

    # use opposite condition to filter only wanted row
    rows_to_update = ~ rows_to_exclude
    updated_df = updated_df[rows_to_update]
    
    # remove duplicate based on column
    updated_df = remove_duplicates(updated_df, 'Mailing Street')

    # create new file name, create path, save file
    new_file_name = f'{file[:-25]}.xlsx'
    new_file_path = os.path.join(folder_path, new_file_name)
    updated_df.to_excel(new_file_path, index=False)
    
    return original_df, updated_df, excluded_df, new_file_name

