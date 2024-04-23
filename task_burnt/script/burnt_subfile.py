import pandas as pd

# create dataframe with column for UTS
def initalize_uts_file_format():
    uts_column_format = {
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
        'Description':[],
        'DRTV Time':[],
        'Bank':[],
        'Unique Id':[],
        'Membership No':[],
        }
    
    return pd.DataFrame(uts_column_format)

# function to copy data from current df to df with UTS format
def copy_data(new_df, df):
    new_df['Donor Id'] = df['Supporter ID']
    new_df['Title'] = df['Title']
    new_df['First Name'] = df['First Name']
    new_df['Last Name'] = df['Last Name']
    new_df['Ethnic'] = df['Ethnic']
    new_df['Gender'] = df['Gender']
    new_df['Street'] = df['Mailing Street']
    new_df['City'] = df['Mailing City']
    new_df['State'] = df['Mailing State/Province']
    new_df['Post Code'] = df['Mailing Zip/Postal Code']
    new_df['Country'] = df['Mailing Country']
    new_df['Home Phone'] = df['Home Phone']
    new_df['Work Phone'] = df['Work Phone']
    new_df['Mobile Phone'] = df['Mobile']
    new_df['Email'] = df['Email']
    new_df['Date of Birth'] = df['Birthdate']
    new_df['National Id'] = df['National ID']
    new_df['Donation Amount'] = df['Original Pledge Amount']
    new_df['Last Pledge Date'] = df['Last Donation Date']
    new_df['Pledge id'] = df['Pledge ID']
    new_df['Pledge Date'] = df['Signup Date']
    new_df['Pledge Start Date'] = df['Start Date']
    new_df['Pledge End Date'] = df['End Date']
    new_df['Payment Method'] = df['Payment Method']
    new_df['Payment Submethod'] = df['Payment Submethod']
    new_df['Truncated CC'] = df['Card Number (Partial Only)']
    new_df['Expiry Date'] = df['Card Expiry']
    new_df['Frequency'] = df['Pledge Frequency']
    new_df['Campaign'] = '7015g000000pEbS'
    new_df['Campaign Name'] = 'TM Burnt Activation'
    new_df['Description'] = 'TM Burnt Reactivation'
    
    return new_df