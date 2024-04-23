

def process_mobile_numbers(df):
    # remove empty space and hyphens
    df['Mobile Phone'] = df['Mobile Phone'].str.replace(r'[ +\-]', '', regex=True)
    df['Mobile Phone'] = df['Mobile Phone'].apply(lambda x: reformat_mobile_number(x))
    
    return df

def reformat_mobile_number(x):

    if x.startswith('011') and len(x) == 11:
        return x[:3] + '-' + x[3:]
    elif x.startswith('01') and len(x) == 10:
        return x[:3] + '-' + x[3:]
    else:
        return x
    
def count_invalid_phone_number(df, column_name):

    mask = (
        (df[column_name].astype(str).apply(len) < 11) | 
        (df[column_name].astype(str).apply(len) > 12) |
        (~ df[column_name].str.startswith('01'))
        
        )
    
    row_count = len(df[mask])

    return row_count