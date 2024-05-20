import calendar
import datetime

def clean_birthdate_file(df):
    df['National ID'] = df['National ID'].apply(validate_nat_id)
    df['Birthdate'] = df['National ID'].apply(calculate_birthdate)
    df['Age'] = df['Birthdate'].apply(calculate_age)
    return df


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

