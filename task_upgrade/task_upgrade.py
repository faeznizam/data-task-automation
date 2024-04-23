from .script import uts_file_format
from .script import copy_data_upgrade
from .script import remove_duplicate
from .script import clean_phone_number

import os
import pandas as pd
import warnings

def main(folder_path):
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    for file in os.listdir(folder_path):
        

        file_path = os.path.join(folder_path, file)

        df = pd.read_excel(file_path)

        new_df = uts_file_format.initalize_uts_file_format()

        new_df = copy_data_upgrade.copy_data_upgrade(new_df, df)

        new_df = clean_phone_number.process_mobile_numbers(new_df)

        new_df = remove_duplicate.remove_duplicates(new_df)

        new_file_name = f'{file[:-12]}.xlsx'

        new_file_path = os.path.join(folder_path, new_file_name)

        new_df.to_excel(new_file_path, index=False)

        print(f'{new_file_name} has been saved')

        

        

    