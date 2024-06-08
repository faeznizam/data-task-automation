import os

from dependencies import process_onetime_conversion


def one_time_conversion_flow():
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_onetimeconversion'

    # check file
    if any('TMOC' in file for file in os.listdir(folder_path)):
        print('Files already been processed! Please check the folder') 
    else:
        deleted_list = []
        processed_file_info = []

        # process file
        for file_name in os.listdir(folder_path):
            if 'TM One Time' in file_name:
                
                # process file
                original_df, updated_df, excluded_df, new_file_name = process_onetime_conversion.process_file(folder_path, file_name)
                
                # get deleted rows
                process_onetime_conversion.get_deleted_info(excluded_df, deleted_list, new_file_name)
                
                # get row count
                process_onetime_conversion.get_row_count(original_df, updated_df, new_file_name, processed_file_info)

            # create deleted list
            process_onetime_conversion.create_deleted_list(deleted_list, folder_path)

            # create analysis table
            process_onetime_conversion.analysis_table(processed_file_info)

            print('Process completed.')


if __name__ == '__main__':
    one_time_conversion_flow()