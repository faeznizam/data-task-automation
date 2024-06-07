import os

from dependencies import process_onetime_conversion


def one_time_conversion_flow():
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_onetimeconversion'

    # check file
    if any('TMOC' in file for file in os.listdir(folder_path)):
        print('Files already been processed! Please check the folder') 
    else:
        # process file
        for file_name in os.listdir(folder_path):
            if 'TM One Time' in file_name:
                # process file
                pass

            
        

        

if __name__ == '__main__':
    one_time_conversion_flow()