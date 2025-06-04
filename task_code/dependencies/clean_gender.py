import re
from datetime import datetime

def extract_and_validate_yymmdd(x):
  if len(x) == 12:
    match = re.search(r'\d{6}', x)
    
    if match:
      yymmdd = match.group(0)

      # get 2 digit number for current year
      current_yy = int(datetime.today().strftime("%y"))
      input_yy = int(yymmdd[:2])

      # categorize century
      century = 1900 if input_yy > current_yy else 2000
      full_year = century + input_yy

      full_date_str = f"{full_year}{yymmdd[2:]}"  # YYYYMMDD string

      try:
        # Validate date
        datetime.strptime(full_date_str, "%Y%m%d")

        # Reformat the full 12-char cleaned ID with dashes
        return f"{x[:6]}-{x[6:8]}-{x[8:]}"
      
      except ValueError:
        return None
          
  return None

def gender_by_national_id(df):
  # match pattern
  national_id_pattern = re.compile(r'^\d{6}-\d{2}-\d{4}$')

  # function to determine gender by last digit in national id
  def determine_gender(national_id):
    return 'Female' if int(national_id[-1]) % 2 == 0 else 'Male'

  df['Gender'] = df['Updated National ID'].apply(lambda x: determine_gender(x) if x and national_id_pattern.match(x) else '')

  return df

def rename_column(df):
    df.rename(columns = {'Gender' : 'sescore__Gender__c'}, inplace=True)
    df.rename(columns = {'National ID' : 'sescore__National_Id__c'}, inplace=True)

    return df

def columns_to_keep():
  columns = ['Supporter ID', 'sescore__Gender__c']

  return columns



def clean_gender_file(df):
    
    df['Updated National ID'] = (
    df['National ID']
    .str.replace(r'[^A-Za-z0-9]', '', regex=True)
    .apply(lambda x : extract_and_validate_yymmdd(x))
    )

    df = gender_by_national_id(df)

    df = df.drop('Updated National ID', axis=1)

    return rename_column(df)

