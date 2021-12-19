from datamallet.tabular.utils import (check_columns,
                                      extract_col_types,
                                      get_unique,
                                      check_numeric,
                                      unique_count, combine_categorical_columns)
import pandas as pd


def columns_with_distinct_values(df,
                                 maximum_number_distinct_values=3,
                                 categorical_only=True):
    """
    Determines columns in a dataframe whose unique value count is
    less than or equal to the maximum_number_distinct_values
    :param df: pandas dataframe
    :param maximum_number_distinct_values:int, the upper limit on
            the number of distinct values in a column (translates into number of sectors in pie chart).
            A value of 3 is good for pie charts, 7 for boxplots or violin plots.
    :param categorical_only: boolean, whether to include categorical columns only in the final list or not
    :return: a list of column names which conform to the columns
                which have the number of distinct values less than the specified maximum_number_distinct_values
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(maximum_number_distinct_values, int), "maximum_number_sectors must be an integer"
    assert isinstance(categorical_only, bool), "category_only must be a boolean"

    columns_list = list()
    unique_count_dict = unique_count(df=df) # dictionary of column name with count of unique values as key

    col_types = extract_col_types(df=df)
    if categorical_only:
        categorical_cols = combine_categorical_columns(df, col_types)
        for col in df.columns:
            if col not in categorical_cols:
                del unique_count_dict[col] # delete non categorical columns

    for column_name, distinct_count in unique_count_dict.items():
        if distinct_count <= maximum_number_distinct_values:
            columns_list.append(column_name)

    return columns_list


def column_use(df,
               col_types,
               threshold=5):
    """
    This function helps in determining whether a column in a dataframe
       should be used to color the data points in a chart or if it is
        okay for simply naming the points
    :param df: pandas dataframe
    :param col_types: dictionary that contains mapping of column type to list of column names
                    It is the output of extract_col_types in tabular module
    :param threshold: int, think of it as the number
           of distinct colors in a chart(e.g scatterplot)
    :return: a dictionary that decides what columns to be used to color points in a chart,
            and which should be used to name points, they keys are name and hue, values are list of column names
    """
    assert isinstance(col_types, dict), "col_types must be a dictionary"
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(threshold, int), "threshold must be an integer"
    assert 'numeric' in col_types.keys(), "col_types dictionary missing key numeric"
    assert 'object' in col_types.keys(), "col_types dictionary missing key object"
    assert 'boolean' in col_types.keys(), "col_types dictionary missing key boolean"
    assert 'categorical' in col_types.keys(), "col_types dictionary missing key categorical"
    assert 'datetime' in col_types.keys(), "col_types dictionary missing key datetime"
    assert 'timedelta' in col_types.keys(), "col_types dictionary missing key timedelta"
    all_categorical_cols = combine_categorical_columns(df=df, col_types=col_types)

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
    :param figs: python list of plotly graph objects (plotly chart objects).
    :param filename: str, string nmae for file excluding any extension
    :return: None
    """
    assert isinstance(figs, list), "figs is expected to be a list of plotly graph objects"
    assert isinstance(filename, str), "filename must be a string"
    assert '.' not in filename, "no dot should be in filename"
    html_filename = filename+'.html'

    with open(html_filename, 'a') as f:
        for fig in figs:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    return None


def create_pairs(df, numeric_cols):
    """
    Create a non repeat list of tuples which contains pairs of
    numeric cols in df for visualization purpose as x and y axis
    :param df: pandas dataframe
    :param numeric_cols: list of column names which have numeric data, output of extract_numeric_cols(df=df)
    :return: list of tuple of non repeat pairing of columns in numeric_cols
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(numeric_cols, list), "numeric_cols must be a list"
    assert len(numeric_cols) > 2, "the length of numeric_cols must be greater than 2"

    passed_cols = set()
    pairs = list()

    if check_columns(df=df,column_list=numeric_cols) and check_numeric(df=df,column_list=numeric_cols):
        for col1 in numeric_cols:
            for col2 in numeric_cols:
                if col1 == col2:
                    continue

                if len(passed_cols) == 0 or col2 not in passed_cols:
                    pairs.append((col1,col2))

            passed_cols.add(col1)

    return pairs


def hierarchical_path(df,col_types, limit=3):
    """
    It helps to determine the path for a tree map or sunburst chart (hierarchical charts),
    the idea is to start the path from the column with the
    least number of unique values to the one with the most
    :param df: pandas dataframe
    :param col_types: dictionary that contains mapping of column type to list of column names
                    It is the output of extract_col_types in tabular module
    :param limit: the number of elements in the path list,
                i.e maximum number of treemap/sunburst categories
    :return:sorted_cols: list of column names which are categorical in nature,
            starting with the columns with least number of unique to the most.
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(limit, int), "limit must be a int"
    assert limit >1, "limit must be at least 2, to have a meaningful hierarchical chart"
    assert isinstance(col_types, dict), "col_types must be a dictionary"
    assert 'numeric' in col_types.keys(), "col_types dictionary missing key numeric"
    assert 'object' in col_types.keys(), "col_types dictionary missing key object"
    assert 'boolean' in col_types.keys(), "col_types dictionary missing key boolean"
    assert 'categorical' in col_types.keys(), "col_types dictionary missing key categorical"
    assert 'datetime' in col_types.keys(), "col_types dictionary missing key datetime"
    assert 'timedelta' in col_types.keys(), "col_types dictionary missing key timedelta"

    col_list = list()
    sorted_cols = list()

    col_list.extend(col_types['object'])
    col_list.extend(col_types['boolean'])
    col_list.extend(col_types['categorical'])

    if len(col_list) > 1:
        unique_counts = [len(get_unique(df=df,col_name=x)) for x in col_list]
        sorted_columns = [col_name for _,col_name in sorted(zip(unique_counts, col_list))]
        sorted_cols = sorted_columns[:limit]

    return sorted_cols













