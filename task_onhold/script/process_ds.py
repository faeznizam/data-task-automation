import pandas as pd


def read_file(file_path):

    df = pd.read_excel(file_path, dtype={'Post Code' : str})

    return df

def populate_campaign(df, file):
    if 'DS - CC 1 Month Prior to Card Expiry' in file:
        df['Campaign'] = '7015g000000h3rdAAA'
        df['Campaign Name'] = 'Card Pre Expiry Campaign'
        df['Description'] = 'Card Pre Expiry Campaign'
    
    elif 'DS - Debit Card Expiry Date' in file:
        df['Campaign'] = '7015g000000h3rdAAA'
        df['Campaign Name'] = 'Card Pre Expiry Campaign'
        df['Description'] = 'Card Pre Expiry Campaign'

    elif 'New Onhold HR Report - DS' in file:
        df['Campaign'] = '7015g000000pEcxAAE'
        df['Campaign Name'] = 'OnHold DS HR Month 1'
        df['Description'] = 'OnHold DS HR Month 1'
    
    return df

def remove_duplicates(df):
    column_to_check_duplicate = 'Mobile Phone'
    df.drop_duplicates(subset = column_to_check_duplicate, keep = 'first', inplace = True)

    return df

def save_file(df, file_path, file):
    df.to_excel(file_path, index=False)

    print(f'{file} has been save to folder')