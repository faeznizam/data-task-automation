import re
import os

def remove_timestamp(folder_path):

    for file_name in os.listdir(folder_path):

        original_path = os.path.join(folder_path, file_name)

        pattern = r'-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}'
        cleaned_name = re.sub(pattern, '', file_name)

        new_path = os.path.join(folder_path, cleaned_name)

        os.rename(original_path, new_path)

