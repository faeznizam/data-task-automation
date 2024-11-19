import logging
import pandas as pd
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def delete_column(df, filename):
    

    delete_column_list = [
        'Donor Id','Title','First Name','Last Name','Ethnic','Gender','Street','City','State',
        'Post Code','Country','Home Phone','Work Phone','Mobile Phone','Email','Date of Birth',
        'National Id','Last Pledge Amount','Last Pledge Date','Last Cash Amount','Last Cash Date',
        'Pledge id','Pledge Date','Pledge Start Date','Pledge End Date','Donation Amount',
        'Payment Method','Payment Submethod','Frequency','Cardholder Name',
        'Gift Date','Bank Account Holder Name','Bank Account Number','Bank','DRTV Time','Unique Id',
        'Membership No','Action','Description','Campaign','Campaign Name',
        'DRTV Channel','Creative','Result']
    
    df = df.drop(columns=delete_column_list)

    return df

def rename_column(df, filename):
    

    if 'VSMC_SF' in filename:
        df = df.rename(columns={
        'Truncated CC' : 'sescore__Card_Number_Masked__c',
        'Expiry Date' : 'sescore__Card_Expiry__c',
        'External Pledge Reference Id' : 'sescore__External_Pledge_Reference_Id__c',
        'iPay88 Tokenized ID' : 'sescore__Card_Token__c'
        })

    elif 'Token_SF' in filename:
        df = df.rename(columns={
        'Truncated CC' : 'sescore__Card_Number_Masked__c',
        'Expiry Date' : 'sescore__Card_Expiry__c',
        'External Pledge Reference Id' : 'sescore__Pledge_Id__c',
        'iPay88 Tokenized ID' : 'sescore__Card_Token__c'
        })

    return df
     
def rename_file(filename):
    
    return f'{filename[:-5]}.csv'

def analyze_file(df, filename):
    

    condition = df['Result'] != 'Tokenized OK'

    if condition.any():
        logging.info(f'{condition.sum()} data from {filename} not tokenized!')
    else:
        logging.info(f'All data in {filename} has been tokenized!')

def process_file(folder_path, filename):
    
    file_path = os.path.join(folder_path, filename)
    
    
    df = pd.read_excel(file_path)

    analyze_file(df, filename)
    df = delete_column(df, filename)
    df = rename_column(df, filename)
    new_file_name = rename_file(filename)

    
    df.to_csv(os.path.join(folder_path, new_file_name), index=False)

    
    logging.info('Process complete')

def token_return_main(folder_path):

    # for test data use this
    #folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\task_code\test_data\task_token_return_file'

    for filename in os.listdir(folder_path):
        if 'VSMC_SF' in filename:
            process_file(folder_path, filename)
        elif 'Token_SF' in filename:
            process_file(folder_path, filename)
    


#if __name__ == '__main__':
    #token_return_main()


