import datetime
import calendar
import re

def clean_ic_file(df):
    df['Updated National ID'] = df['National ID'].apply(validate_nat_id)
    df = blank_invalid_ic(df)
    return rename_column(df)

def validate_nat_id(national_id):
  # change data type
  national_id = str(national_id)

  # Remove hyphens and spaces
  national_id_cleaned = national_id.replace("-", "").replace(" ", "")

  # Check if the cleaned national ID has a length of 12
  if len(national_id_cleaned) == 12:
    # check if nat_id valid using is_valid_date function, then return restructured format
    if is_valid_date(national_id_cleaned):
      return f"{national_id_cleaned[:6]}-{national_id_cleaned[6:8]}-{national_id_cleaned[8:]}"
  
  return national_id

def is_valid_date(national_id):
  # get the first 6 number and assign to year month and day
  if len(national_id) == 12:
    year = national_id[0:2]
    month = national_id[2:4]
    day = national_id[4:6]

    # get current year
    current_year = datetime.datetime.now().year % 100

    # Determine the century based on the last 2 digits in the year. If year less and equal to current year
    # then century = 20
    if int(year) <= current_year:
        century = 20
    else:
        century = 19

    # Check if the month is valid
    if 1 <= int(month) <= 12:
        # Check if the day is valid for the given month
        max_day = calendar.monthrange(century * 100 + int(year), int(month))[1]
        if 1 <= int(day) <= max_day:
            return True

    return False
  
def blank_invalid_ic(df):
   # match pattern
   national_id_pattern = re.compile(r'^\d{6}-\d{2}-\d{4}$')

   # apply nat id pattern, blank if not match
   df['Updated National ID'] = df['Updated National ID'].apply(lambda x: x if national_id_pattern.match(x) else '')
   
   return df 

def rename_column(df):
    df.rename(columns = {'Updated National ID' : 'sescore__National_Id__c'}, inplace=True)

    return df
