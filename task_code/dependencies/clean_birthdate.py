
from datetime import datetime
import re


"""

def validate_nat_id(national_id):

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
  
# function to calculate birthdate
def calculate_birthdate(national_id):
   if len(national_id) == 14:
      # get the first 6 number and assign to year month and day
      year = national_id[0:2]
      month = national_id[2:4]
      day = national_id[4:6]

      # get last 2 digit of current year 
      current_year = datetime.datetime.now().year % 100
      
      # logic to get the first 2 digit based on last 2 digit
      if int(year) <= current_year:
         century = 20
      else:
         century = 19
         
      # check if the month and day in respective range and reformat into birtdate 
      if month and  1 <= int(month) <= 12:
         if day and 1 <= int(day) <= 31:
            birthdate = f"{century}{year}-{month}-{day}"
            return birthdate
      
         else:
            return None
      else:
         return None
 
def calculate_age(birthdate):
   # if the birthdate column is empty then return None
   if birthdate is None:
      return None
   
   # get current year
   current_year = datetime.datetime.now().year
   # get birth year from birthdate
   birth_year = int(birthdate[:4])

   age = current_year - birth_year

   return age 

"""

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
        return f'{full_date_str[:4]}' + '-' + f'{full_date_str[4:6]}' + '-' + f'{full_date_str[6:]}'
      
      except ValueError:
        return None
          
  return None

def columns_to_keep():
  columns = ['Supporter ID', 'Birthdate']

  return columns

def clean_birthdate_file(df):

   df['Birthdate'] = (
      df['National ID']
      .str.replace(r'[^A-Za-z0-9]', '', regex=True)
      .apply(lambda x : extract_and_validate_yymmdd(x))
      )
   
   return df


      

