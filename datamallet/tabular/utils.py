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


def check_numeric(df,column_list):
    """
    Checks whether column_list is a subset of all numeric columns
    :param df:
    :param column_list:
    :return:
    """
    assert isinstance(column_list, list), "column_list must be a list"
    assert isinstance(df, pd.DataFrame), "df must be a dataframe"

    numeric_cols = extract_numeric_cols(df=df)
    return set(column_list).issubset(set(numeric_cols))


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
    :param df: pandas dataframe
    :param col_name:str, name of column in pandas dataframe
    :return:
    """
    assert isinstance(col_name, str), "col_name must be a string"
    assert isinstance(df, pd.DataFrame)
    unique_values = None

    if check_columns(df=df, column_list=[col_name]):
        unique_values = df[col_name].unique()
    return unique_values


def unique_count(df):
    """
    Determine the number of unique values for each column in the
    dataframe and returns as a dictionary with col name as key and number of distinct values as value
    :param df: pandas dataframe
    :return: dictionary mapping column name in a dataframe to the number of unique values in that column
    """
    unique_count_dict = dict()

    if check_dataframe(df=df):
        for col in df.columns:
            unique_values = get_unique(df=df, col_name=col)
            unique_count_dict[col] = len(unique_values)

    return unique_count_dict


def extract_numeric_cols(df):
    """
    Utility function for obtaining all numeric columns in a dataframe
    :param df: pandas dataframe
    :return: list of column names of numeric type
    """
    numeric_cols=None

    if check_dataframe(df=df):
        numeric_df = df.select_dtypes(include='number')
        numeric_cols = list(numeric_df.columns)

    return numeric_cols


def extract_object_cols(df):
    """
    Extract columns with object data type from the dataframe
    :param df: pandas dataframe
    :return: list of column names of object type
    """
    object_cols = None

    if check_dataframe(df=df):

        object_df = df.select_dtypes(include='object')
        object_cols = list(object_df.columns)

    return object_cols


def extract_datetime_cols(df):
    """
    Extract columns with datetime data type from the dataframe
    :param df: pandas dataframe
    :return: list of column names of datetime type
    """
    datetime_cols = None

    if check_dataframe(df=df):
        datetime_df = df.select_dtypes(include='datetime')
        datetime_cols = list(datetime_df.columns)

    return datetime_cols


def extract_timedelta_cols(df):
    """
    Extract columns with timedelta data type from the dataframe
    :param df: pandas dataframe
    :return: list of column names of timedelta type
    """
    time_cols=None

    if check_dataframe(df=df):
        timedelta_df = df.select_dtypes(include='timedelta')
        time_cols = list(timedelta_df.columns)

    return time_cols


def extract_categorical_cols(df):
    """
    Extract columns with categorical data type from the dataframe
    :param df: pandas dataframe
    :return: list of column names of categorical type
    """
    category_cols = None

    if check_dataframe(df=df):
        category_df = df.select_dtypes(include='category')
        category_cols = list(category_df.columns)

    return category_cols


def extract_bool_cols(df):
    """
    Extract columns with boolean data type from the dataframe
    :param df: pandas dataframe
    :return: list of column names of boolean type
    """
    boolean_cols = None

    if check_dataframe(df=df):

        boolean_df = df.select_dtypes(include='bool')
        boolean_cols = list(boolean_df.columns)

    return boolean_cols


def extract_datetimetz_cols(df):
    """
    Extract columns with datetimetz data type from the dataframe
    :param df: pandas dataframe
    :return: list of column names of datetimetz type
    """
    datetime_cols = None

    if check_dataframe(df=df):
        datetime_df = df.select_dtypes(include='datetimetz')
        datetime_cols = list(datetime_df.columns)

    return datetime_cols


def extract_col_types(df):
    """
    Extract the different column types as a dictionary
    where the key is the column type (numeric, boolean, datetime ...)
    and the value is the list of column names of that type in the dataframe.
    :param df: pandas dataframe
    :return: dictionary containing data type and list of column names mapping
    """
    assert isinstance(df, pd.DataFrame), 'df must be of type pandas dataframe'
    numeric_columns = extract_numeric_cols(df=df)
    boolean_columns = extract_bool_cols(df=df)
    datetime_columns = extract_datetime_cols(df=df)
    timedelta_columns = extract_timedelta_cols(df=df)
    object_columns = extract_object_cols(df=df)
    categorical_columns = extract_categorical_cols(df=df)
    timezone_cols = extract_datetimetz_cols(df=df)

    datetime_columns.extend(timezone_cols)

    column_type = {
        'numeric':numeric_columns,
        'object':object_columns,
        'boolean':boolean_columns,
        'categorical':categorical_columns,
        'datetime':datetime_columns,
        'timedelta':timedelta_columns
    }

    return column_type


def calculate_correlation(df, method='pearson'):
    """
    Calculates the correlation of the entire dataframe based on the specified method
    :param df: pandas dataframe
    :param method:str, one of pearson, kendall or spearman used to compute the correlation
    :return:
    """
    assert method in ['pearson', 'kendall', 'spearman'], 'method must be one of pearson, kendall or spearman'
    corr = None

    check = check_dataframe(df)

    if check:
        corr = df.corr(method=method)

    return corr


def combine_categorical_columns(df, col_types):
    """
    Combined columns of types categorical, object, and boolean into a list
    :param df: pandas dataframe
    :param col_types: dictionary that contains mapping of column type to list of column names
                    It is the output of extract_col_types in tabular module
    :return: a list of column names of types categorical, object, or boolean
    """
    assert isinstance(col_types, dict), "col_types must be a dictionary with column " \
                                        "name as keys and column type as value"
    assert 'numeric' in col_types.keys(), "col_types dictionary missing key numeric"
    assert 'object' in col_types.keys(), "col_types dictionary missing key object"
    assert 'boolean' in col_types.keys(), "col_types dictionary missing key boolean"
    assert 'categorical' in col_types.keys(), "col_types dictionary missing key categorical"
    assert 'datetime' in col_types.keys(), "col_types dictionary missing key datetime"
    assert 'timedelta' in col_types.keys(), "col_types dictionary missing key timedelta"

    combined = list()

    if check_dataframe(df=df):

        categorical = col_types['categorical']
        object_cols = col_types['object']
        boolean_cols = col_types['boolean']

        combined.extend(categorical)
        combined.extend(object_cols)
        combined.extend(boolean_cols)

    return combined
