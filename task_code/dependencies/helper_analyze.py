from tabulate import tabulate
import logging

def get_row_count(original_df, updated_df, new_file_name, processed_file_info):
    # append row count for before and after to list in dictionary.
    processed_file_info.append({
        'File Name' : new_file_name,
        'Before Clean' : len(original_df),
        'After Clean' : len(updated_df),
    }) 
    
def analysis_table(processed_file_info):
    logging.info('\n')
    logging.info(tabulate(processed_file_info, headers="keys", tablefmt="html"))



    



