import pandas as pd
import os

# function to process every file
def process_data(file_path, folder_path, file, date, status, closed_reason, column_to_drop):
    # read file
    df = pd.read_excel(file_path)

    # rename file based on process
    if status == 'Burnt':
        df = df.rename(columns={'Pledge ID': 'Id'})
    elif status == 'Rejected':
        df = df.rename(columns={'Pledge ID': 'Id'})

    # populate column with date, status, and closed reason accordingly. 
    df['npsp__EndDate__c'] = date
    df['npsp__Status__c'] = status
    df['npsp__ClosedReason__c'] = closed_reason

    # remove row
    df.drop(columns=column_to_drop, inplace=True)

    # save file to excel and csv
    df.to_excel(os.path.join(folder_path, f'{file[:-25]}_to_upload.xlsx'), index=False)
    #df.to_csv(os.path.join(folder_path, f'{file[:-25]}_to_upload.csv'), index=False, encoding='utf-8')

# function for burnt file
def process_burnt(file_path, folder_path, file, date):
    # get column to delete
    column_to_drop_burnt = [
        'Supporter ID', 'First Name', 'Last Name', 'Signup Date', 'First Donation Date', 'End Date', 
        'Campaign: Campaign Name', 'Pledge Frequency', 'Status', 'Stage'
    ]

    # process the file
    process_data(file_path, folder_path, file, date, 'Burnt', 'Burnt', column_to_drop_burnt)

# function for rejected file
def process_reject(file_path, folder_path, file, date):
    # get column to delete
    column_to_drop_reject = [
        'Supporter ID', 'First Name', 'Last Name', 'Signup Date', 'First Donation Date', 'Last Donation Date', 
        'End Date', 'Campaign: Campaign Name', 'Status', 'Stage', 'Pledge Frequency'
    ]

    # process the file. 
    process_data(file_path, folder_path, file, date, 'Rejected', 'Soft Reject', column_to_drop_reject)
