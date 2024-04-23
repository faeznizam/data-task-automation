# import dependency
import pandas as pd

# create dataframe with column for UTS
# this create empty table with column as follows

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


    
