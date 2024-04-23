def remove_duplicates(df):
    column_to_check_duplicate = 'Mobile Phone'
    df.drop_duplicates(subset = column_to_check_duplicate, keep = 'first', inplace = True)

    #print('Duplicates has been removed')

    return df