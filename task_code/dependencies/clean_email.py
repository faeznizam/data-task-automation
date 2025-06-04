def check_email(email):
    if email.startswith('noemail'):
        return ''
    
    corrections = {
        'gmail.cim': 'gmail.com',
        'gmail.cm': 'gmail.com',
        'gmail.cn': 'gmail.com',
        'gmail.om': 'gmail.com'
    }

    for wrong, correct in corrections.items():
        if wrong in email:
            return email.replace(wrong, correct)
        
    return email
    
    

def rename_column(df):
    df.rename(columns = {'Email' : 'Original Email'}, inplace=True)

    return df

def columns_to_keep():
  columns = ['Supporter ID', 'Email', 'npe01__HomeEmail__c', 'npe01__Preferred_Email__c', 'npe01__WorkEmail__c']

  return columns

# create 3 column with new column name
def clean_email_file(df):

    df = rename_column(df)
    df['Email'] = df['Original Email'].apply(check_email)
    df['npe01__HomeEmail__c'] = df['Original Email'].apply(check_email)
    df['npe01__Preferred_Email__c'] = df['Original Email'].apply(check_email)
    df['npe01__WorkEmail__c'] = df['Original Email'].apply(check_email)
    
    return df



