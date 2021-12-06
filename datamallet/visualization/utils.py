from datamallet.tabular.utils import (extract_numeric_cols,
                                      extract_col_types,
                                      get_unique,
                                      check_dataframe,
                                      unique_count)
import pandas as pd


def pie_sectors(df, maximum_number_sectors=3):
    """
    Determines columns in a dataframe whose unique value count is
    less than or equal to the maximum number of sectors
    :param df:
    :param maximum_number_sectors:int, the upper limit on
            the number of sectors you desire in your pie chart.
            The number of sectors in a pie chart translates to the number of unique entries in a column.
    :return: a list of column names which conform to the columns
                which have the number of distinct values less than the specified maximum
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
    :return: a list of column names of types categorical, object, and boolean
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
    :return: a dictionary that decides what columns to be used to color points in a chart,
            and which should be used to name points
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


def figures_to_html(figs, filename):
    """
    Utility function that creates a single html file when given the list of plotly graph objects
    :param figs: python list of plotly graph objects
    :param filename: str, string nmae for file excluding any extension
    :return: None
    """
    assert isinstance(figs, list), "figs is expected to be a list of plotly graph objects"
    assert isinstance(filename, str), "filename must be a string"
    html_filename = filename+'.html'

    with open(html_filename, 'a') as f:
        for fig in figs:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    return None


def create_pairs(df):
    """
    Create a non repeat list of tuples which contains pairs of
    numeric cols in df for visualization purpose as x and y axis
    :param df: pandas dataframe
    :return: list of tuple of non repeat pairing
    """

    numeric_cols = extract_numeric_cols(df=df)
    passed_cols = set()
    pairs = list()

    for col1 in numeric_cols:
        for col2 in numeric_cols:
            if col1 == col2:
                continue

            if len(passed_cols) == 0 or col2 not in passed_cols:
                pairs.append((col1,col2))

        passed_cols.add(col1)

    return pairs


def treemap_path(df, limit=3):
    """
    It helps to determine the path for a tree map or sunburst chart,
    the idea is to start the path from the column with the
    least number of unique values to the one with the most
    :param df: pandas dataframe
    :param limit: the number of elements in the path list,
                i.e maximum number of treemap/sunburst categories
    :return:
    """
    check = check_dataframe(df=df)
    col_list = list()
    sorted_cols = None

    if check:
        column_type = extract_col_types(df)

        col_list.extend(column_type['object'])
        col_list.extend(column_type['boolean'])
        col_list.extend(column_type['categorical'])

        unique_counts = [len(get_unique(df=df,col_name=x)) for x in col_list]

        sorted_columns = [col_name for _,col_name in sorted(zip(unique_counts, col_list))]

        sorted_cols = sorted_columns[:limit]

    return sorted_cols













