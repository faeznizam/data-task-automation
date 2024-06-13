import pandas as pd

def create_startek_table():
    startek_format = {
        'DONOR': [],
        'TITLE': [],
        'FNAME': [],
        'LNAME': [],
        'Optional Line': [],
        'Race': [],
        'ADD': [],
        'ADD2': [],
        'ADD3': [],
        'CITY': [],
        'ST': [],
        'ZIP': [],
        'IPAY ID': [],
        'SERIAL NO': [],
        'PH_HOME': [],
        'PH_WORK': [],
        'PH_CELL': [],
        'EMAIL': [],
        'NOMAIL': [],
        'REASON': [],
        'NOEMAIL': [],
        'NOTELEMARK': [],
        'BIRTH_DT': [],
        'PAYMENT TYPE': [],
        'IN_AMT1': [],
        'IN_AMT2': [],
        'LS_AMT1': [],
        'LS_AMT2': [],
        'IN_DT1': [],
        'IN_DT2': [],
        'LS_DT1': [],
        'LS_DT2': [],
        'IC_NO': [],
        'PL_ID': [],
        'PL_START': [],
        'PL_END': [],
        'PL_AMT': [],
        'PL_ACC': [],
        'PL_EXP': [],
        'PL_FREQ': [],
        'GIFT_DATE': [],
        'GIFT_AMT' : [],
        'STATUS': [],
        'NOTES': [],
        'SOL': [],
        'ListCode': [],
        'PKG': [],
        'Contact ID': [],
        'Date - Contact': [],
        'Activity': [],
        'Gender': [],
        'SIGN UP DATE': [],
        'CC_TYPE': []
    }

    return pd.DataFrame(startek_format)

df_strtk = create_startek_table()


def copy_data_startek(df_strtk, df_file):
  df_strtk['DONOR'] = df_file['Donor Id']
  df_strtk['TITLE'] = df_file['Title']
  df_strtk['FNAME'] = df_file['First Name']
  df_strtk['LNAME'] = df_file['Last Name']
  df_strtk['Race'] = df_file['Ethnic'].apply(lambda x: 'M' if x == 'Malay' else 'I' if x == 'Indian' else 'O' if x == 'Others' else 'C' if x == 'Chinese' else '')
  df_strtk['ADD'] = df_file['Street']
  df_strtk['CITY'] = df_file['State']
  df_strtk['ZIP'] = df_file['Post Code']
  df_strtk['PH_HOME'] = df_file['Home Phone']
  df_strtk['PH_WORK'] = df_file['Work Phone']
  df_strtk['PH_CELL'] = df_file['Mobile Phone']
  df_strtk['EMAIL'] = df_file['Email']
  df_strtk['NOMAIL'] = 'N'
  df_strtk['NOEMAIL'] = 'N'
  df_strtk['NOTELEMARK'] = 'N'
  df_strtk['PAYMENT TYPE'] = df_file['Payment Submethod'].apply(lambda x: 'VS' if x == 'Visa' else 'MC' if x == 'Mastercard' else 'AX' if x == 'Amex' else '')
  df_strtk['IN_AMT1'] = '0'
  df_strtk['IN_AMT2'] = '0'
  df_strtk['LS_AMT1'] = '0'
  df_strtk['LS_AMT2'] = df_file['Donation Amount']
  df_strtk['IC_NO'] = df_file['National Id']
  df_strtk['PL_ID'] = df_file['Pledge id']
  df_strtk['PL_START'] = df_file['Pledge Start Date']
  df_strtk['PL_AMT'] = df_file['Donation Amount']
  df_strtk['PL_ACC'] = df_file['Truncated CC']
  df_strtk['PL_EXP'] = df_file['Expiry Date']
  df_strtk['PL_FREQ'] = df_file['Frequency'].apply(lambda x: 'M' if x == 'Monthly' else 'SM' )
  df_strtk['STATUS'] = 'T8'
  df_strtk['SOL'] = 'RC001'
  df_strtk['ListCode'] = 'T07'
  df_strtk['Date - Contact'] = pd.Timestamp('now').strftime('%d-%m-%Y')
  df_strtk['Gender'] = df_file['Gender'].apply(lambda x: 'M' if x == 'Male' else 'F' if x == 'Female' else 'O' if x == 'Other' else '')

  return df_strtk


def populate_pkg_column(file, df):
   if 'HR' in file:
      df['PKG'] = 'HR'  
   else:
      df['PKG'] = 'SR'
    
   return df