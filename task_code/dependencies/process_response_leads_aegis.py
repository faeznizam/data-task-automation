# import dependency
import pandas as pd



# create empty dataframe with UTS column format
def create_aegis_table():
    aegis_column_format = {
        'Donor Id': [],
        'Title': [],
        'First Name': [],
        'Last Name':[],
        'Ethnic':[],
        'Gender':[],
        'Street':[],
        'City':[],
        'State':[],
        'Post Code':[],
        'Country':[],
        'Home Phone':[],
        'Work Phone':[],
        'Mobile Phone':[],
        'Email':[],
        'Date of Birth':[],
        'National Id':[],
        'Last Pledge Amount':[],
        'Last Cash Amount':[],
        'Last Pledge Date':[],
        'Last Cash Date':[],
        'Pledge id':[],
        'Pledge Date':[],
        'Pledge Start Date':[],
        'Pledge End Date':[],
        'Donation Amount':[],
        'Payment Method':[],
        'Payment Submethod':[],
        'Truncated CC':[],
        'Expiry Date':[],
        'Frequency':[],
        'Cardholder Name':[],
        'Gift Date':[],
        'Campaign':[],
        'Campaign Name':[],
        'Bank Account Holder Name':[],
        'Bank Account Number':[],
        'Preferred Change Date' : [],
        'Action' : [],
        'Description':[],
        'DRTV Time':[],
        'Bank':[],
        'Unique Id':[],
        'Membership No':[],
        'iPay88 Tokenized ID' : [],
        }
    
    return pd.DataFrame(aegis_column_format)

def date_from_filename(filename, df):

    date = f'{filename[14:20]}'
    filedate = f'{date[4:6]}-{date[2:4]}-{date[0:2]}'

    df['Preferred Change Date'] = filedate



    return df

# function to copy data from current df to df with UTS format
def copy_data_to_new_table(new_df, df):
    new_df['Donor Id'] = df['DONOR']
    new_df['Title'] = df['TITLE']
    new_df['First Name'] = df['FNAME']
    new_df['Last Name'] = df['LNAME']
    new_df['Action'] = 'Unsuccessful Calls'
    new_df['Description'] = df['Final Sub Status']

    return new_df

def populate_campaign(df, file):
    if 'HR' in file:
        df['Campaign'] = '7015g000000pFWRAA2'
        df['Campaign Name'] = 'OnHold Startek HR'

    elif 'SR' in file:
        df['Campaign'] = '7015g000000pFWEAA2'
        df['Campaign Name'] = 'OnHold Startek SR'
    
    return df


def remove_successful_response(df):
    condition = df['STATUS'] != 'TA'
    df = df[condition]

    return df
