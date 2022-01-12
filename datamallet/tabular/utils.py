import pandas as pd


def time_index(df):
    """
    Checks to see if the index of the dataframe is a datetime object
    :param df: pandas dataframe that needs to be checked for a time index
    :return: True or False

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import time_index
    >>> df4 = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':[2,3,4,5,6],'D':[4,7,2,5,7],
       ... 'E':['1/2/2019','1/3/2019','1/4/2019','1/5/2019','1/6/2019'],
       ... 'F':['1/3/2019','1/4/2019','1/5/2019','1/6/2019','1/8/2019'],})
    >>> df4.index = pd.to_datetime(df4['E'])

    >>> time_index(df=df4)
    True

    """
    assert isinstance(df, pd.DataFrame), 'df must be a pandas dataframe object'

    return isinstance(df.index, pd.core.indexes.datetimes.DatetimeIndex)


def check_dataframe(df):
    """
    Checks to see that the provided object is a pandas dataframe
    :param df: pandas dataframe
    :return: bool

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import check_dataframe

    >>> df = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':['dog','cat', 'sheep','dog','cat'],
        ... 'D':['male','male','male','female','female'],'E':[True,True,False,True,True]})

    >>> check_dataframe(df=df)
    True

    """
    if isinstance(df, pd.DataFrame):
        return True
    else:
        return False


def check_dictionary(df, column_dict):
    """
    Checks the keys of a dictionary to see if it belongs to columns in a dataframe.
    :param df:pandas dataframe
    :param column_dict: dictionary that needs to be checked to see of its keys are column names
    :return:boolean, whether the keys of the dictionary are column names

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import check_dictionary
    >>> df = pd.DataFrame({'A': [1, 2, 3, 4, 5],'B': [2, 4, 6, 8, 10],'C': ['dog', 'cat', 'sheep', 'dog', 'cat'],
        ... 'D': ['male', 'male', 'male', 'female', 'female'],
        ... 'E': [True, True, False, True, True]})
    >>> check_dictionary(df=df, column_dict={'A':2,'B':3})
    True
    >>> check_dictionary(df=df, column_dict={'A':2,'Z':3})
    False

    """
    assert isinstance(column_dict, dict), "column_dict must be a dictionary"
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"

    length_dictionary = len(column_dict)
    df_cols = df.columns

    columns_count = 0

    for key,value in column_dict.items():
        if key in df_cols:
            columns_count += 1

    return columns_count == length_dictionary


def check_columns(df, column_list):
    """
    Checks to see if provided column_list is part of dataframe columns
    :param df: pandas dataframe
    :param column_list: list of column names
    :return: bool, whether all columns in column_list are in df.columns

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import check_columns
    >>> df = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':['dog','cat', 'sheep','dog','cat'],
        ... 'D':['male','male','male','female','female'],'E':[True,True,False,True,True]})

    >>> check_columns(df=df, column_list=['A'])
    True

    >>> check_columns(df=df, column_list=['A','B])
    True

    >>> check_columns(df=df, column_list=['Z','A'])
    False
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
    :return:bool

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import check_numeric
    >>> df = pd.DataFrame({'A':[1,2,3,4,5],
        ... 'B':[2,4,6,8,10],'C':['dog','cat', 'sheep','dog','cat'],'D':['male','male','male','female','female'],
        ... 'E':[True,True,False,True,True]})

    >>> check_numeric(df=df, column_list=['A'])
    True

    >>> check_numeric(df=df, column_list=['C','D'])
    False

    """
    assert isinstance(column_list, list), "column_list must be a list"
    assert isinstance(df, pd.DataFrame), "df must be a dataframe"

    numeric_cols = extract_numeric_cols(df=df)
    return set(column_list).issubset(set(numeric_cols))


def check_categorical(df, column_list):
    """
    Checks whether column_list ia a subset of all categorical columns
     (Categorical columns are columns of the types - Categorical, object or boolean.
    :param df:
    :param column_list:
    :return:bool

    >>> import pandas as pd
    >>> from datamallet.tabular.utils import check_categorical
    >>> df = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':['dog','cat', 'sheep','dog','cat'],'D':['male','male','male','female','female'],'E':[True,True,False,True,True]})
    >>> df['D'] = df['D'].astype('category')
    >>> check_categorical(df=df, column_list=['C','D'])
    True

    >>> check_categorical(df=df, column_list=['C', 'D', 'E','A'])
    False

    >>> check_categorical(df=df, column_list=['A', 'B'])
    False

    """
    assert isinstance(column_list, list), "column_list must be a list"
    assert isinstance(df, pd.DataFrame), "df must be a dataframe"
    col_types = extract_col_types(df=df)
    combined_categorical = combine_categorical_columns(df=df,
                                                       col_types=col_types)

    return set(column_list).issubset(set(combined_categorical))


def column_mean(df, skipna=True, numeric_only=True,
                column_list=None):
    """
    Calculates the mean value for all columns in dataframe
    :param df: pandas dataframe
    :param skipna:boolean, whether to skip Na values in mean calculation
    :param numeric_only: boolean, to include only numeric columns
    :param column_list: list, column_list is list of column names for which to calculate the mean
    :return: pandas series

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import column_mean
    >>> df3 = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':[2,3,4,5,6],
                   'D':[4,7,2,5,7],
                   })

    >>> column_mean(df=df3)['A']
    3.0
    """
    mean = None

    assert isinstance(df, pd.DataFrame), 'df must be of type dataframe'
    assert isinstance(skipna, bool), 'skipna must be boolean'
    assert isinstance(numeric_only, bool), 'numeric_only must be boolean'
    assert isinstance(column_list, list) or column_list is None, "column_list must be a list or None"

    if column_list is None:
        mean = df.mean(skipna=skipna,numeric_only=numeric_only)
    if isinstance(column_list, list):
        if check_numeric(df=df, column_list=column_list):
            mean = df.loc[:,column_list].mean(skipna=skipna,numeric_only=numeric_only)

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

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import get_unique
    >>> df = pd.DataFrame({'C':['dog','cat', 'sheep','dog','cat'],'D':['male','male','male','female','female']})
    >>> print(get_unique(df=df, col_name='C'))
    ['dog' 'cat' 'sheep']

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

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import unique_count
    >>> df = pd.DataFrame({'A':[1,2,3,4,5],
       ... 'B':[2,4,6,8,10],'C':['dog','cat', 'sheep','dog','cat'],
       ... 'D':['male','male','male','female','female'],'E':[True,True,False,True,True]})

    >>> unique_count(df=df)
    {'A': 5, 'B': 5, 'C': 3, 'D':2, 'E':2}
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

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import extract_numeric_cols
    >>> df = pd.DataFrame({'A':[1,2,3,4,5], 'B':[2,4,6,8,10],
        ... 'C':['dog','cat', 'sheep','dog','cat'],
        ... 'D':['male','male','male','female','female'],'E':[True,True,False,True,True]})

    >>> extract_numeric_cols(df=df)
    ['A','B']

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

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import extract_object_cols
    >>> df = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':['dog','cat', 'sheep','dog','cat'],
        ... 'D':['male','male','male','female','female'],
        ... 'E':[True,True,False,True,True]})

    >>> df['D'] = df['D'].astype('category')

    >>> extract_object_cols(df=df)
    ['C']
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

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import extract_datetime_cols
    >>> df4 = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':[2,3,4,5,6],'D':[4,7,2,5,7],
        ... 'E':['1/2/2019','1/3/2019','1/4/2019','1/5/2019','1/6/2019'],
        ... 'F':['1/3/2019','1/4/2019','1/5/2019','1/6/2019','1/8/2019'],
                   })
    >>> df4.index = pd.to_datetime(df4['E'])
    >>> df4['E'] = pd.to_datetime(df4['E'])
    >>> df4['F'] = pd.to_datetime(df4['F'])
    >>> df4['G'] = df4['F'] - df4['E']

    >>> extract_datetime_cols(df=df4)
    ['E','F']

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

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import extract_timedelta_cols
    >>> df4 = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':[2,3,4,5,6],'D':[4,7,2,5,7],
        ... 'E':['1/2/2019','1/3/2019','1/4/2019','1/5/2019','1/6/2019'],
        ... 'F':['1/3/2019','1/4/2019','1/5/2019','1/6/2019','1/8/2019'],})
    >>> df4.index = pd.to_datetime(df4['E'])
    >>> df4['E'] = pd.to_datetime(df4['E'])
    >>> df4['F'] = pd.to_datetime(df4['F'])
    >>> df4['G'] = df4['F'] - df4['E']

    >>> extract_timedelta_cols(df=df4)
    ['G']
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

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import extract_categorical_cols
    >>> df = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':['dog','cat', 'sheep','dog','cat'],
        ... 'D':['male','male','male','female','female'],'E':[True,True,False,True,True]})

    >>> df['D'] = df['D'].astype('category')

    >>> extract_categorical_cols(df=df)
    ['D']
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

    Usage
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':['dog','cat', 'sheep','dog','cat'],
        ... 'D':['male','male','male','female','female'],'E':[True,True,False,True,True]})

    >>> df['D'] = df['D'].astype('category')

    >>> extract_bool_cols(df=df)
    ['E']
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

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import extract_col_types
    >>> df = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':['dog','cat', 'sheep','dog','cat'],
        ... 'D':['male','male','male','female','female'],'E':[True,True,False,True,True]})

    >>> df['D'] = df['D'].astype('category')

    >>> extract_col_types(df=df)
    {'numeric': ['A', 'B'],
    'object': ['C'],
    'boolean': ['E'],
    'categorical': ['D'],
    'datetime': [],
    'timedelta': []}


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
    :return: Correlation matrix

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import calculate_correlation
    >>> df = pd.DataFrame({"B": [0, 1, 2, 4],"A": [0, 1, 0,  4]})

    >>> calculate_correlation(df=df, method='spearman')
              B         A
    B  1.000000  0.632456
    A  0.632456  1.000000
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

    Usage
    >>> import pandas as pd
    >>> from datamallet.tabular.utils import combine_categorical_columns
    >>> df = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':['dog','cat', 'sheep','dog','cat'],
        ... 'D':['male','male','male','female','female'],'E':[True,True,False,True,True]})

    >>> df['D'] = df['D'].astype('category')

    >>> col_types = {'numeric': ['A', 'B'], 'object': ['C'], 'boolean': ['E'], 'categorical': ['D'], 'datetime': [],
                'timedelta': []}

    >>> combine_categorical_columns(df=df, col_types=col_types)
    ['D','C','E']

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
