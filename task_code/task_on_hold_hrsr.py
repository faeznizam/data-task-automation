# import module from folder
from .dependencies import process_startek_file
from .dependencies import startek_format
from .dependencies import process_uts
from .dependencies import process_ds
from .dependencies import mobile_phone_handler
from .dependencies import duplication_handler

# import dependencies
from tabulate import tabulate
import pandas as pd
import warnings
import logging
import time
import os

# function for different process
def startek_process(file_path, file, folder_path):

   # read file
   original_df = pd.read_excel(file_path, dtype={'Post Code': str})

   # initialize new dataframe with new format and move data to new dataframe
   updated_df = startek_format.initialize_startek_format()
   updated_df = startek_format.copy_data(updated_df, original_df)
   updated_df = startek_format.populate_pkg_column(file, updated_df)

   # clean phone number column
   updated_df = mobile_phone_handler.process_mobile_numbers(updated_df, 'PH_CELL')

   # exclude invalid number rows and assign to new dataframe
   rows_to_exclude = mobile_phone_handler.delete_condition(updated_df, 'PH_CELL')
   excluded_df = updated_df[rows_to_exclude]

   # use opposite condition to filter the wanted number
   rows_to_update = ~ rows_to_exclude
   updated_df = updated_df[rows_to_update]

   # delete duplicate based on phone number column
   updated_df = duplication_handler.remove_duplicates(updated_df, 'PH_CELL')

   # rename file and save file
   new_file_name = process_startek_file.rename_startek_file(file)
   process_startek_file.save_file(updated_df, new_file_name, folder_path)

   return original_df, updated_df, new_file_name, excluded_df

def uts_process(file_path, file, folder_path):

   # read file
   df = process_uts.read_file(file_path)
   modified_df = df
   modified_df = process_uts.populate_campaign(modified_df, file)
   modified_df = mobile_phone_handler.process_mobile_numbers(modified_df, 'Mobile Phone')
   modified_df = duplication_handler.remove_duplicates(modified_df, 'Mobile Phone')
   new_file_name = process_uts.rename_uts_file(file)
   process_uts.save_file(modified_df, new_file_name, folder_path)

   return df, modified_df, new_file_name

def ds_process(file_path, file):
   df = process_ds.read_file(file_path)
   modified_df = df
   modified_df = process_ds.populate_campaign(modified_df, file)
   modified_df = mobile_phone_handler.process_mobile_numbers(modified_df, 'Mobile Phone')
   modified_df = duplication_handler.remove_duplicates(modified_df, 'Mobile Phone')

   return df, modified_df

def task_onhold_hrsr_main(folder_path):
   # add start time to record code runtime
   start_time = time.time()

   # ignore warning
   warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

   logging.info('Processing On Hold HRSR Files ...')

   #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_onhold'
   #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\TM Schedule Files\Hard and Soft Reject\2024\May - Copy'

   processed_file_info = []
   deleted_list = []
   deleted_list_startek = []

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
               original_df, updated_df, new_file_name, excluded_df = startek_process(file_path, file, sub_folder_path)

               # check if the df is not empty then append to deleted_list
               if not excluded_df.empty:
                  # add file name so that I know where the row belongs
                  excluded_df['File Name'] = new_file_name
                  deleted_list_startek.append(excluded_df)        

               processed_file_info.append({
                  'File Name' : new_file_name, # get file name
                  'Before Clean' : len(original_df), # count before clean
                  'After Clean' : len(updated_df), # count after clean
               })

   # combine all df that has been append to list and save the file in excel
   # empty list gave out False boolean
   if deleted_list:
      final_deleted_df = pd.concat(deleted_list, ignore_index=True)
      final_deleted_df.to_excel(os.path.join(folder_path, 'deleted_list_startek.xlsx'), index=False)
   else:
      logging.info('Deleted list was not created since there is no data!')# combine all df that has been append to list and save the file in excel

   # print process status and analysis
   logging.info('Process completed!. Files has been saved in selected folder.')
   
   
         
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
               })
   logging.info('Processing UTS File Completed!')
   logging.info(f'{len(os.listdir(sub_folder_path))} files has been saved in folder')

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
   logging.info(f'{output_filename} has been save to folder')

   processed_file_info.append({
      'File Name' : output_filename, # get file name
      'Before Clean' : 'NA', # count before clean
      'After Clean' : len(combine_df), # count after clean
   })


   logging.info('Processing DS File Completed!')
   logging.info(f'{len(os.listdir(ds_folder))} files has been saved in folder')


   # print completion status
   logging.info('On Hold HRSR Files has been processed completely!')
   # print the list in table form
   logging.info(tabulate(processed_file_info, headers="keys", tablefmt="grid"))

   # get end time for runtime and print
   end_time = time.time()
   code_runtime = end_time - start_time
   logging.info('Processing Time: {:2f} seconds'.format(code_runtime))

