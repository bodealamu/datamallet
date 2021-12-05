from datamallet.tabular.utils import (extract_numeric_cols,
                                      extract_col_types,
                                      get_unique,
                                      check_dataframe,
                                      unique_count,
                                      calculate_correlation)
import plotly.express as px
import pandas as pd


def pie_sectors(df, maximum_number_sectors=3):
    """
    Determines columns in a dataframe whose unique value count is
    less than or equal to the maximum number of sectors
    :param df:
    :param maximum_number_sectors:int,
    :return:
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(maximum_number_sectors, int), "maximum_number_sectors must be an integer"

    columns_list = list()
    unique_count_dict = unique_count(df=df)

    for column, count in unique_count_dict.items():
        if count <= maximum_number_sectors:
            columns_list.append(column)

    return columns_list

