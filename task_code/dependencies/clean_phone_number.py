


# function
def process_mobile_numbers(df):
  # set data type to string
  df['Mobile'] = df['Mobile'].astype(str)

  df['Updated Mobile'] = df['Mobile']

  df['Updated Mobile'] =  df['Updated Mobile']
 
  # remove empty space and hyphens
  df['Updated Mobile'] = df['Updated Mobile'].str.replace(r'[A-Za-z +\-]', '', regex=True)

  # handle numbers starting with 60, 060, 600, 06001, 001, 1, 65
  df['Updated Mobile'] = df['Updated Mobile'].apply(lambda x: process_prefix(x))

  # add 0 in front of the startswith 1 and lenght 9 and 10
  df['Updated Mobile'] = df['Updated Mobile'].apply(lambda x: '0' + x if x.startswith('1') and len(x) in {9, 10} else x)

  # add a hyphen after the 3rd digit for number startswith 0 and add hyphen after 2nd digit for number startwith 65
  df['Updated Mobile'] = df['Updated Mobile'].apply(lambda x: x[:3] + '-' + x[3:] if x.startswith('0') else (x[:2] + '-' + x[2:] if x.startswith('65') else x))
  
  return df

def process_prefix(x):
    if x.startswith('601'):
        return x[2:]
    elif x.startswith(('0601', '6001', '06001')):
        return x[3:]
    elif x.startswith('1') and len(x) in {9, 10}:
        return x
    elif x.startswith(('01', '011')) and len(x) in {10, 11}:
        return x
    elif x.startswith(('61', '001', '0001', '65')):
        return x
    else:
        return ''


def rename_column(df):
    df.rename(columns = {'Updated Mobile' : 'MobilePhone'}, inplace=True)

    return df

def columns_to_keep():
  columns = ['Supporter ID', 'MobilePhone']

  return columns

# process file
def clean_phone_file(df):
    df = process_mobile_numbers(df)
    return rename_column(df)