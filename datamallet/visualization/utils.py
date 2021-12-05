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


def __combine_object_categorical(df):
    """
    Combined columns of types categorical, object, and boolean into a list
    :param df: pandas dataframe
    :return:
    """

    combined = list()

    if check_dataframe(df=df):
        col_types = extract_col_types(df=df)

        categorical = col_types['categorical']
        object_cols = col_types['object']
        boolean_cols = col_types['boolean']

        combined.extend(categorical)
        combined.extend(object_cols)
        combined.extend(boolean_cols)

    return combined


def column_use(df, threshold=5):
    """
    This function helps in determining whether a column in a dataframe
       should be used to color the data points in a chart or if it is
        okay for simply naming the points
    :param df: pandas dataframe
    :param threshold: int, think of it as the number
           of distinct colors in a chart(e.g scatterplot)
    :return:
    """
    all_categorical_cols = __combine_object_categorical(df=df)

    number_of_rows = df.shape[0]

    column_use_dict = dict()
    names_list = list()
    hue_list = list()

    for col in all_categorical_cols:
        number_of_unique = len(get_unique(df=df, col_name=col))
        ratio = number_of_rows / number_of_unique

        if ratio < threshold:
            names_list.append(col)

        else:
            hue_list.append(col)

    column_use_dict['name'] = names_list
    column_use_dict['hue'] = hue_list

    return column_use_dict


