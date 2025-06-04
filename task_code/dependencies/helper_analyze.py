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


def get_row_count_and_amount(original_df, updated_df, new_file_name, processed_file_info):
    # Ensure 'Donation Amount' column is numeric
    if 'Donation Amount' in updated_df.columns:
        total_amount = updated_df['Donation Amount'].astype(float).sum()
    else:
        total_amount = 0  # Default to 0 if column is missing

    # Append row count and amount to the dictionary list
    processed_file_info.append({
        'File Name': new_file_name,
        'Before Clean': len(original_df),
        'After Clean': len(updated_df),
        'Total Amount': total_amount
    })


