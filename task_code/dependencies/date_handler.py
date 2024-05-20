from datetime import datetime
import pandas as pd

# create date format in YYYY-MM-DD for current year
def current_date_format():
    current_date = datetime.now()
    date_format = current_date.strftime('%Y-%m-%d')
    return date_format

# convert date format from / to -
def convert_date_format(df):
    df['Created Date'] = pd.to_datetime(df['Created Date'], format='%d/%m/%Y')
    df['Created Date'] = df['Created Date'].dt.strftime('%Y-%m-%d')

    return df