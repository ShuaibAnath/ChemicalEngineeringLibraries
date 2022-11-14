def check_columns(df_check_cols, columns):
    # Check if specified columns exist in Dataframe
    are_cols_in_df = True
    for column in columns:
        if column not in df_check_cols:
            are_cols_in_df = False
    return are_cols_in_df


def check_for_nulls(df_check_nulls):
    # Check for any nulls in Dataframe
    are_nulls_in_df = False
    if df_check_nulls.isnull().values.any():
        are_nulls_in_df = True
    return are_nulls_in_df


def get_number_of_zeros(df_count_zeros, column_name_str=None):
    # Count number of zeros in all columns of Dataframe
    count = 0
    if column_name_str is None:
        for column_name in df_count_zeros.columns:
            column = df_count_zeros[column_name]
            count += (column == 0).sum()
    else:
        # Count number of zeros in column named column_name
        count = (df_count_zeros[column_name_str] == 0).sum()
    return count


def check_for_negative(*values):
    # Check for a negative value in a collection of values
    has_negative_value = False
    values_list = [*values]
    for value in values_list:
        if value < 0:
            has_negative_value = True
    return has_negative_value


def check_for_zeros(*values):
    # Check for a negative value in a collection of values
    has_zero_value = False
    values_list = [*values]
    for value in values_list:
        if value == 0:
            has_zero_value = True
    return has_zero_value


def check_for_non_positive(*values):
    # Check for a non-positive value in a collection of values
    has_non_positive_value = False
    values_list = [*values]
    for value in values_list:
        if value <= 0:
            has_non_positive_value = True
    return has_non_positive_value


def check_df_dtypes(df_data):
    is_data_type_int64_or_float64 = True
    data_types_dict = {0: 'int64', 1: 'float64'}
    for column in df_data:
        if str(df_data[column].dtypes) != data_types_dict[0] and str(df_data[column].dtypes) != data_types_dict[1]:
            is_data_type_int64_or_float64 = False
    return is_data_type_int64_or_float64
