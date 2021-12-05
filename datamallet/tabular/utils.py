import pandas as pd


def time_index(df):
    """
    Checks to see if the index of the dataframe is a datetime object
    :param df: pandas dataframe that needs to be checked for a time index
    :return:
    """
    assert isinstance(df, pd.DataFrame), 'df must be a pandas dataframe object'

    return isinstance(df.index, pd.core.indexes.datetimes.DatetimeIndex)