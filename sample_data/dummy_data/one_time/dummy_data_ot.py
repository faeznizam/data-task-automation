from faker import Faker
import pandas as pd
import os
import random

fake = Faker()

num_rows = 20

data = []

for _ in range(num_rows):

    def donor_id_generator():
        middle_number = ''.join([str(random.randint(0,9)) for _ in range(6)])
        return f'S{middle_number}M1'
    
    def phone_number():
        second_digit = random.choice([2,3,4,5,6,7,8,9])
        remaining_digit = ''.join([str(random.randint(0,9)) for _ in range(6)])
        return f'01{second_digit}-{remaining_digit}'
    
    def national_id():
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%y%m%d')
        random_part = f"{random.randint(1, 99):02d}"
        random_digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"{birth_date}-{random_part}-{random_digits}"
    
    
    
    data.append({

        'Donor Id':	donor_id_generator(), 
        'Title'	: random.choice(['Mr.', 'Ms.', 'Mrs.', 'Dr.', 'Prof.']),
        'First Name' :	fake.first_name(),
        'Last Name'	: fake.last_name(),
        'Ethnic' :	random.choice(['Malay', 'Chinese', 'Indian', 'Others']),
        'Gender' :	random.choice(['Male', 'Female']),
        'Street' :	fake.street_address(),
        'City' :	fake.city(),
        'State' :	fake.state(),
        'Post Code' : fake.postcode(),
        'Country' :	fake.country(),
        'Home Phone' : phone_number(),
        'Work Phone' : phone_number(),
        'Mobile Phone' : phone_number(),
        'Email' :	fake.email(),
        'Date of Birth' : fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%d/%m/%Y'),
        'National Id' :	national_id(),
        'Last Pledge Amount' :	'0',
        'Last Cash Amount' : random.randint(0, 10000),
        'Last Pledge Date' : '',
        'Last Cash Date' : '',
        'Pledge id' :'',
        'Pledge Date' : '',
        'Pledge Start Date' : '',
        'Pledge End Date' :	'',
        'Donation Amount' : '',
        'Payment Method' :	'',
        'Payment Submethod' : '',
        'Truncated CC' : '',
        'Expiry Date' :	'',
        'Frequency' : '',
        'Cardholder Name' :	'',
        'Gift Date' : 	'',
        'Campaign' : ''.join([str(random.randint(0,9)) for _ in range(15)]),
        'Campaign Name' : random.choice(['Campaign 1', 'Campaign 2', 'Campaign 3']),
        'Bank Account Holder Name' : '',	
        'Bank Account Number' : '',
        'Description' :	'',
        'DRTV Time' : '',
        'Bank' : '',
        'Unique Id' : '',
        'Membership No' : '',
    })

df = pd.DataFrame(data)

folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\PortableApp\sample_data\dummy_data\one_time'

df.to_excel(os.path.join(folder_path, 'TM One Time Conversion To Pledge - sample data.xlsx'), index=False)

print('Done')

