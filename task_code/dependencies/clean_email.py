
def clean_email_file(df):

    df = rename_column(df)
    df['Email'] = df['Original Email'].apply(check_email)
    df['npe01__HomeEmail__c'] = df['Original Email'].apply(check_email)
    df['npe01__Preferred_Email__c'] = df['Original Email'].apply(check_email)
    df['npe01__WorkEmail__c'] = df['Original Email'].apply(check_email)
    return df

def check_email(email):
    if email.startswith('noemail'):
        return ''
    else:
        return email
    

def rename_column(df):
    df.rename(columns = {'Email' : 'Original Email'}, inplace=True)

    return df

