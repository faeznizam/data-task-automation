from datetime import datetime
import os



def remove_duplicates(df):
    column_to_check_duplicate = 'PH_CELL'
    df.drop_duplicates(subset = column_to_check_duplicate, keep = 'first', inplace = True)

    return df

def rename_startek_file(file):
    current_date = datetime.now()
    date_format = current_date.strftime('%y%m%d')
    extract_file_number = file[-7:-5]
    
    if 'HR' in file:
        return f'TM_AG_HR_OH{extract_file_number}_{date_format}.xlsx'
    elif 'SR' in file:
        return f'TM_AG_SR_OH{extract_file_number}_{date_format}.xlsx'
    else:
        pass
        

def save_file(df, new_filename, folder_path):
    new_file_path = os.path.join(folder_path, new_filename)
    df.to_excel(new_file_path, index=False)

    print(f'{new_filename} has been saved in the folder')