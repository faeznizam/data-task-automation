import pandas as pd
import os
from dependencies import process_response_leads_aegis

def process_response_leads_aegis_flow(filename, folder_path):
    file_path = os.path.join(folder_path, filename)

    original_df = pd.read_excel(file_path)

    updated_df = process_response_leads_aegis.create_aegis_table()
    updated_df = process_response_leads_aegis.copy_data_to_new_table(updated_df, original_df)
    updated_df = process_response_leads_aegis.populate_campaign(updated_df, filename)

    new_file_name = f'{filename[:-4]}.xlsx'
    updated_df.to_excel(os.path.join(folder_path, new_file_name), index=False)


def response_leads_aegis_main():

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\sample_data\test_data\task_response_leads_aegis'
    
    for filename in os.listdir(folder_path):
        if 'TM_AG_HR' in filename:
            process_response_leads_aegis_flow(filename, folder_path)
        elif 'TM_AG_SR' in filename:
            process_response_leads_aegis_flow(filename, folder_path)
            
            
        


if __name__ == '__main__':
    response_leads_aegis_main()