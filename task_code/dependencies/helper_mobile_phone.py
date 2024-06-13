

def process_mobile_numbers(df, column):
    # remove empty space and hyphens
    df[column] = df[column].str.replace(r'[A-Za-z +\-]', '', regex=True)
    df[column] = df[column].apply(lambda x: reformat_mobile_number(x))
    
    return df

def reformat_mobile_number(x):

    if x.startswith('011') and len(x) == 11:
        return x[:3] + '-' + x[3:]
    elif x.startswith('01') and len(x) == 10:
        return x[:3] + '-' + x[3:]
    elif x.startswith(('6010', '6012', '6013', '6014', '6015', '6016', '6017', '6018', '6019')) and len(x) == 11:
        return x[1:4] + '-' + x[4:]
    elif x.startswith('6011') and len(x) == 12:
        return x[1:4] + '-' + x[4:]
    else:
        return x
    
def delete_condition(df, column_name):

    condition1 = (df[column_name].str.startswith('011')) & (df[column_name].str.len() != 12)
    condition2 = df[column_name].str.contains(r'^01[0-9&&[^1]]-') & (df[column_name].str.len() != 11)
    condition3 = ~df[column_name].str.startswith('01')
    condition4 = ~df[column_name].str.contains(r'^01\d+-')

    mask = (condition1 | condition2 | condition3 | condition4)
    
    

    return mask