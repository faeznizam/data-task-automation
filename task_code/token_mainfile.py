# import function from subfile
from dependencies import token_subfile

# import dependency
import os
import pandas as pd
import numpy as np

# main function
def main():
    
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\TM Schedule Files\Tokenization\2024\May\09'

    files = os.listdir(folder_path)

    # using for loop to detect file based on file name and process accordingly
    for file_name in files:
        if 'vsmc' in file_name.lower():
            token_subfile.process_egfile(folder_path, file_name)
        elif 'new card' in file_name.lower():
            token_subfile.process_new_tokenfile(folder_path, file_name)
        else:
            print('No File Available')

if __name__ == '__main__':
    main()
