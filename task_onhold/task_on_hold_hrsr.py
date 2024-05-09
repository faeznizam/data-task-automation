from script import process_startek_file
from script import startek_format
from script import process_uts
from script import process_ds
from script import clean_phone_number
from script import remove_duplicate

import pandas as pd
import os
import warnings
from tabulate import tabulate

def startek_process(file_path, file, folder_path):
   df = pd.read_excel(file_path, dtype={'Post Code': str})
   modified_df = startek_format.initialize_startek_format()
   modified_df = startek_format.copy_data(modified_df, df)
   modified_df = startek_format.populate_pkg_column(file, modified_df)
   modified_df = clean_phone_number.process_mobile_numbers(modified_df, 'PH_CELL')
   modified_df = remove_duplicate.remove_duplicates(modified_df, 'PH_CELL')
   new_file_name = process_startek_file.rename_startek_file(file)
   process_startek_file.save_file(modified_df, new_file_name, folder_path)

   return df, modified_df, new_file_name

def uts_process(file_path, file, folder_path):
   df = process_uts.read_file(file_path)
   modified_df = df
   modified_df = process_uts.populate_campaign(modified_df, file)
   modified_df = clean_phone_number.process_mobile_numbers(modified_df, 'Mobile Phone')
   modified_df = remove_duplicate.remove_duplicates(modified_df, 'Mobile Phone')
   new_file_name = process_uts.rename_uts_file(file)
   process_uts.save_file(modified_df, new_file_name, folder_path)

   return df, modified_df, new_file_name

def ds_process(file_path, file):
   df = process_ds.read_file(file_path)
   modified_df = df
   modified_df = process_ds.populate_campaign(modified_df, file)
   modified_df = clean_phone_number.process_mobile_numbers(modified_df, 'Mobile Phone')
   modified_df = remove_duplicate.remove_duplicates(modified_df, 'Mobile Phone')

   return df, modified_df

def main():
   warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

   print('Processing On Hold HRSR Files ...')

   #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_onhold\test_data\Apr'
   folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\TM Schedule Files\Hard and Soft Reject\2024\May - Copy'

   processed_file_info = []
   # startek
   agency = 'Startek'
   agency_folder = os.path.join(folder_path, agency)
   for sub_folder in os.listdir(agency_folder):
      if sub_folder in ['HR', 'SR']:
         sub_folder_path = os.path.join(agency_folder, sub_folder)
         file_list = os.listdir(sub_folder_path)
         for file in file_list:
            if 'New Onhold' in file:
               file_path = os.path.join(sub_folder_path, file)
               df, modified_df, new_file_name = startek_process(file_path, file, sub_folder_path)
               processed_file_info.append({
                  'File Name' : new_file_name, # get file name
                  'Before Clean' : len(df), # count before clean
                  'After Clean' : len(modified_df), # count after clean
                  'Invalid Phone Number' : clean_phone_number.count_invalid_phone_number(modified_df, 'PH_CELL') # flag invalid mobile number
               })
      
   print('Processing Startek File Completed!')
   print(f'{len(os.listdir(sub_folder_path))} files has been saved in folder')
         
   # UTS 
   agency2 = 'UTS'
   agency_folder2 = os.path.join(folder_path, agency2)
   for sub_folder in os.listdir(agency_folder2):
      if sub_folder in ['HR', 'SR']:
         sub_folder_path = os.path.join(agency_folder2, sub_folder)
         file_list2 = os.listdir(sub_folder_path)
         for file in file_list2:
            if 'New Onhold' in file:
               file_path = os.path.join(sub_folder_path, file)
               df, modified_df, new_file_name = uts_process(file_path, file, sub_folder_path)
               processed_file_info.append({
                  'File Name' : new_file_name, # get file name
                  'Before Clean' : len(df), # count before clean
                  'After Clean' : len(modified_df), # count after clean
                  'Invalid Phone Number' : clean_phone_number.count_invalid_phone_number(modified_df, 'Mobile Phone') # flag invalid mobile number
               })
   print('Processing UTS File Completed!')
   print(f'{len(os.listdir(sub_folder_path))} files has been saved in folder')

   # DS
   agency3 = 'DS'
   ds_folder = os.path.join(folder_path, agency3)
   file_list = os.listdir(ds_folder)
   for file in file_list:
      if 'DS - CC 1 Month Prior to Card Expiry' in file:
         file_path = os.path.join(ds_folder, file)
         df, modified_df = ds_process(file_path, file)
         new_file_name = 'DS - CC 1 Month Prior to Card Expiry - Processed.xlsx'
         new_file_path = os.path.join(ds_folder, new_file_name)
         process_ds.save_file(modified_df, new_file_path)

      elif 'DS - Debit Card Expiry Date' in file:
         file_path = os.path.join(ds_folder, file)
         df, modified_df = ds_process(file_path, file)
         new_file_name = 'DS - Debit Card Expiry Date - Processed.xlsx'
         new_file_path = os.path.join(ds_folder, new_file_name)
         process_ds.save_file(modified_df, new_file_path)

      elif 'New Onhold HR Report' in file:
         file_path = os.path.join(ds_folder, file)
         df, modified_df = ds_process(file_path, file)
         new_file_name = 'OnHold DS HR Month 1.xlsx'
         new_file_path = os.path.join(ds_folder, new_file_name)
         process_ds.save_file(modified_df, new_file_path)

      else:
         pass

      processed_file_info.append({
         'File Name' : new_file_name, # get file name
         'Before Clean' : len(df), # count before clean
         'After Clean' : len(modified_df), # count after clean
         'Invalid Phone Number' : clean_phone_number.count_invalid_phone_number(modified_df, 'Mobile Phone') # flag invalid mobile number
                     })


   # combine cc and debit file
   file1 = 'DS - CC 1 Month Prior to Card Expiry - Processed.xlsx'
   file2 = 'DS - Debit Card Expiry Date - Processed.xlsx'
   file_path1 = os.path.join(ds_folder, file1)
   file_path2 = os.path.join(ds_folder, file2)
   df1 = pd.read_excel(file_path1)
   df2 = pd.read_excel(file_path2)
   combine_df = pd.concat([df1,df2], ignore_index=True)
   output_filename = 'Card Pre Expiry Campaign.xlsx'
   output_filepath = os.path.join(ds_folder, output_filename)
   combine_df.to_excel(output_filepath, index=False)
   print(f'{output_filename} has been save to folder')

   processed_file_info.append({
      'File Name' : output_filename, # get file name
      'Before Clean' : 'NA', # count before clean
      'After Clean' : len(combine_df), # count after clean
      'Invalid Phone Number' : clean_phone_number.count_invalid_phone_number(combine_df, 'Mobile Phone') # flag invalid mobile number
   })


   print('Processing DS File Completed!')
   print(f'{len(os.listdir(ds_folder))} files has been saved in folder')


   # print completion status
   print('On Hold HRSR Files has been processed completely!')
   # print the list in table form
   print(tabulate(processed_file_info, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
   main()