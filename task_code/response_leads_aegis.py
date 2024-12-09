import pandas as pd
import os
from dependencies import process_response_leads_aegis

def process_response_leads_aegis_flow(filename, folder_path):
    file_path = os.path.join(folder_path, filename)

    original_df = pd.read_excel(file_path)

    original_df = process_response_leads_aegis.remove_successful_response(original_df)
    updated_df = process_response_leads_aegis.create_aegis_table()
    updated_df = process_response_leads_aegis.copy_data_to_new_table(updated_df, original_df)
    updated_df = process_response_leads_aegis.populate_campaign(updated_df, filename)
    updated_df = process_response_leads_aegis.date_from_filename(filename, updated_df)

    new_file_name = f'{filename[:-4]}.xlsx'
    updated_df.to_excel(os.path.join(folder_path, new_file_name), index=False)

    return updated_df




def response_leads_aegis_main():

    
    
    #production
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\TM Schedule Files\Aegis Response Leads\2024\Jun'

    total_row_count = []

    for filename in os.listdir(folder_path):
        if 'TM_AG_HR' in filename:
            updated_df = process_response_leads_aegis_flow(filename, folder_path)
            total_row_count.append(len(updated_df))

        elif 'TM_AG_SR' in filename:
            updated_df = process_response_leads_aegis_flow(filename, folder_path)
            total_row_count.append(len(updated_df))
        
    
    print(f'Total : {sum(total_row_count)}')
            
        


if __name__ == '__main__':
    response_leads_aegis_main()