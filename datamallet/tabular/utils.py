import pandas as pd


def time_index(df):
    """
    Checks to see if the index of the dataframe is a datetime object
    :param df: pandas dataframe that needs to be checked for a time index
    :return:
    """
    assert isinstance(df, pd.DataFrame), 'df must be a pandas dataframe object'

    return isinstance(df.index, pd.core.indexes.datetimes.DatetimeIndex)


def check_dataframe(df):
    """
    Checks to see that the provided object is a pandas dataframe
    :param df: pandas dataframe
    :return: bool
    """
    if isinstance(df, pd.DataFrame):
        return True
    else:
        return False


def check_columns(df, column_list):
    """
    Checks to see if provided column_list is part of dataframe columns
    :param df: pandas dataframe
    :param column_list: list of column names
    :return: bool, whether all columns in column_list are in df.columns
    """
    assert isinstance(column_list, list), "column_list must be a list"
    assert isinstance(df, pd.DataFrame), 'df must be a pandas dataframe'

    actual_columns = df.columns
    length_column_list = len(column_list)
    length_actual_columns = len(actual_columns)

    if length_column_list > length_actual_columns:
        return False

    count = 0
    for col in column_list:
        check = col in actual_columns
        count += check

    return count == length_column_list


def column_mean(df, skipna=True, numeric_only=True):
    """
    Calculates the mean value for all columns in dataframe
    :param df: pandas dataframe
    :param skipna:boolean, whether to skip Na values in mean calculation
    :param numeric_only: boolean, to include only numeric columns
    :return:
    """

    assert isinstance(df, pd.DataFrame), 'df must be of type dataframe'
    assert isinstance(skipna, bool), 'skipna must be boolean'
    assert isinstance(numeric_only, bool), 'numeric_only must be boolean'

    mean = df.mean(skipna=skipna,numeric_only=numeric_only)
    return mean


def get_column_types(df):
    """
    Gets the columns type of each column in the dataframe
    :param df: pandas dataframe
    :return: returns a dictionary with column names as keys and dtypes as value
    """
    column_dictionary = None

    if check_dataframe(df=df):
        column_dictionary = dict(df.dtypes)

    return column_dictionary


def get_unique(df, col_name):
    """
    Gets the unique values in the specified column of that dataframe and returns them
    :param df:
    :param col_name:
    :return:
    """
    unique_values = None

    check = col_name in df.columns

    if check:
        unique_values = df[col_name].unique()
    return unique_values