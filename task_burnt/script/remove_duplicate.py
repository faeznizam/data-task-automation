def remove_duplicates(df, column_to_check_duplicate):
    df.drop_duplicates(subset = column_to_check_duplicate, keep = 'first', inplace = True)

    return df