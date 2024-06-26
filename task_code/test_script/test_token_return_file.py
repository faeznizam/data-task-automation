import pandas as pd
import pytest
from token_return_file import delete_column, rename_column, rename_file, process_file
from unittest.mock import patch, MagicMock
import os

@pytest.fixture
def dummy_data():
    data = {
        'Donor Id' : [None],
        'Title' : [None],
        'First Name' : ['Pakiyavathi'],
        'Last Name' : ['A/P Rajoo'],
        'Ethnic' : [None],
        'Gender' : [None],
        'Street' : [None],
        'City' : [None],
        'State' : [None],
        'Post Code' : [None],
        'Country' : [None],
        'Home Phone': [None],
        'Work Phone' : [None],
        'Mobile Phone' : ['016-9298215'],
        'Email' : ['nillamoon24@gmail.com'],
        'Date of Birth' : [None],
        'National Id' : [None],
        'Last Pledge Amount' : [None],
        'Last Pledge Date' : [None],
        'Last Cash Amount' : [None],
        'Last Cash Date' : [None],
        'Pledge id' : [None],
        'Pledge Date' : [None],
        'Pledge Start Date' : [None],
        'Pledge End Date' : [None],
        'Donation Amount' : [65],
        'Payment Method' : [None],
        'Payment Submethod' : [None],
        'Truncated CC' : ['51********5280'],
        'Expiry Date' : ['05/28'], 
        'Frequency' : ['Monthly'],
        'Cardholder Name' : ['Pakiyavathi Rajoo'],
        'Gift Date' : [None],
        'Bank Account Holder Name' : [None],
        'Bank Account Number' : [None],
        'Bank' : [None],
        'DRTV Time' : [None],
        'Unique Id' : [None],
        'Membership No' : [None],
        'Action' : [None],
        'Description' : [None],
        'Campaign' : [None],
        'Campaign Name' : [None],
        'External Pledge Reference Id' : ['EGIH27168235'], 
        'iPay88 Tokenized ID' : ['7J86tvIIpPrp5280'],
        'DRTV Channel' : [None],
        'Creative' : [None],
        'Result' : ['Tokenized OK']
    }

    df = pd.DataFrame(data)

    return df
    


def test_delete_column():
    df = dummy_data()

    df_cleaned = delete_column(df)
    expected_column = ['Truncated CC', 'Expiry Date', 'External Pledge Reference Id', 'iPay88 Tokenized ID' ]

    assert list(df_cleaned.columns) == expected_column
    assert len(df_cleaned.columns) == 4

def dummy_data2():
    data = {
        'Truncated CC': ['51********5280'],
        'Expiry Date': ['05/28'],
        'External Pledge Reference Id': ['EGIH27168235'],
        'iPay88 Tokenized ID': ['7J86tvIIpPrp5280']
    }
    return pd.DataFrame(data)

def test_rename_column():
    filename_with_vsmc = '1715135847-vsmc_SF.xlsx'
    filename_with_tokensf = 'New Card Token 080524 - To Token_SF.xlsx'
    filename_others = 'asdfsdfsdsdfsf.xlsx'

    df = dummy_data2()

    vsmc_df = rename_column(df, filename_with_vsmc)
    tokensf_df = rename_column(df, filename_with_tokensf)
    others_df = rename_column(df, filename_others)

    expected_column_name_vsmc = [
        'sescore__Card_Number_Masked__c',
        'sescore__Card_Expiry__c',
        'sescore__External_Pledge_Reference_Id__c',
        'sescore__Card_Token__c']
    
    expected_column_name_tokensf = [
        'sescore__Card_Number_Masked__c',
        'sescore__Card_Expiry__c',
        'sescore__Pledge_Id__c',
        'sescore__Card_Token__c'
    ]

    assert list(vsmc_df.columns) == expected_column_name_vsmc
    assert list(tokensf_df.columns) == expected_column_name_tokensf
    assert list(others_df.columns) == list(df.columns)

def test_rename_file():

    filename = '1715135847-vsmc_SF.xlsx'
    expected_filename = '1715135847-vsmc_SF.csv'
    new_filename = rename_file(filename)

    filename2 = '1715135847-vsmc_SF.csv'
    expected_filename = '1715135847-vsmc_SF.csv'
    new_filename2 = rename_file(filename2)

    assert new_filename == expected_filename
    assert new_filename2 != expected_filename


def test_process_file(tmpdir, dummy_data):
    folder_path = tmpdir.mkdir('test_folder')
    filename = 'testfile.xlsx'
    file_path = os.path.join(folder_path, filename)

    dummy_data.to_excel(file_path, index=False)

    new_file_name = 'processedfile.csv'

    with patch('token_return_file.delete_column') as mock_delete_column, \
         patch('token_retrun_file.rename_column') as mock_rename_column, \
         patch('token_return_file.rename file') as mock_rename_file:
        
        # Mock the delete_column, rename_column, and rename_file functions
        mock_delete_column.return_value = dummy_data
        mock_rename_column.return_value = dummy_data
        mock_rename_file.return_value = new_file_name
        
        # Call the function
        process_file(str(folder_path), filename)
        
        # Check that the functions were called correctly
        mock_delete_column.assert_called_once_with(dummy_data)
        mock_rename_column.assert_called_once_with(dummy_data, filename)
        mock_rename_file.assert_called_once_with(filename)
        
        # Check that the new file is created
        new_file_path = os.path.join(folder_path, new_file_name)
        assert os.path.exists(new_file_path)
        
        # Check the contents of the new file
        df_result = pd.read_csv(new_file_path)
        pd.testing.assert_frame_equal(df_result, dummy_data)




 
    


if __name__ == "__main__":
    pytest.main()