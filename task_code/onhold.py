# import module from folder
from .dependencies import process_onhold_startek, process_onhold_uts, process_onhold_ds
from .dependencies import helper_analyze, helper_deletion

# import dependencies
import warnings
import logging
import os



def onhold_flow(folder_path):
   # ignore warning
   warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

   # initiate list
   processed_file_info = []
   deleted_list = []
   deleted_list_startek = []

   # startek process
   # build path for agency folder
   agency_folder = os.path.join(folder_path, 'Startek')
   # loop for subfolder in agency folder
   for sub_folder in os.listdir(agency_folder):
      # if subfolder has HR and SR build subfolderpath
      if sub_folder in ['HR', 'SR']:
         sub_folder_path = os.path.join(agency_folder, sub_folder)
         # inside each subfolder, get file list. 
         file_list = os.listdir(sub_folder_path)
         # check for keyword in all file name
         for file in file_list:
            if 'New Onhold' in file:
               
               # process files
               original_df, updated_df, excluded_df, new_file_name = process_onhold_startek.process_startek(sub_folder_path, file)

               # get deleted rows
               helper_deletion.get_deleted_info(excluded_df, deleted_list_startek, new_file_name)
            
               # get row count
               helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)
               
   # create deleted list
   helper_deletion.create_deleted_list_startek(deleted_list_startek, folder_path)

   logging.info('Startek process completed.')
   
   # process UTS 
   # build folder path for agency folder
   agency_folder = os.path.join(folder_path, 'UTS')

   for sub_folder in os.listdir(agency_folder):

      if sub_folder in ['HR', 'SR']:
         sub_folder_path = os.path.join(agency_folder, sub_folder)

         file_list = os.listdir(sub_folder_path)
         for file in file_list:
            if 'New Onhold' in file:
               
               # process file
               original_df, updated_df, excluded_df, new_file_name = process_onhold_uts.process_uts(sub_folder_path, file)

               # get deleted rows
               helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)
            
               # get row count
               helper_analyze.get_row_count(original_df, updated_df, new_file_name, processed_file_info)

   logging.info('UTS process completed.')

   # process DS
   agency_folder = os.path.join(folder_path, 'DS')

   combine_df, updated_df, excluded_df, new_file_name = process_onhold_ds.process_ds(agency_folder)
 
   # get deleted rows
   helper_deletion.get_deleted_info(excluded_df, deleted_list, new_file_name)
            
   # get row count
   helper_analyze.get_row_count(combine_df, updated_df, new_file_name, processed_file_info)  

   logging.info('DS process completed.')

   # create deleted list
   helper_deletion.create_deleted_list(deleted_list, folder_path)

   # create analysis table
   helper_analyze.analysis_table(processed_file_info)

   logging.info('\nAll Processes completed.')




