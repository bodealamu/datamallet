from datamallet.tabular.utils import (extract_numeric_cols,
                                      check_columns,
                                      check_dataframe,column_mean,
                                      check_categorical,
                                      get_unique,extract_col_types,
                                      unique_count,time_index,
                                      extract_object_cols,
                                      extract_categorical_cols,
                                      extract_bool_cols,extract_datetime_cols,
                                      extract_datetimetz_cols,
                                      extract_timedelta_cols,
                                      calculate_correlation,
                                      combine_categorical_columns,
                                      get_column_types,
                                      check_numeric)
import pandas as pd

# test data, dont alter
df = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female'],
                   'E':[True,True,False,True,True]})

df['D'] = df['D'].astype('category')

df3 = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':[2,3,4,5,6],
                   'D':[4,7,2,5,7],
                   })

df4 = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':[2,3,4,5,6],
                   'D':[4,7,2,5,7],
                    'E':['1/2/2019','1/3/2019','1/4/2019','1/5/2019','1/6/2019'],
                    'F':['1/3/2019','1/4/2019','1/5/2019','1/6/2019','1/8/2019'],
                   })
df4.index = pd.to_datetime(df4['E'])
df4['E'] = pd.to_datetime(df4['E'])
df4['F'] = pd.to_datetime(df4['F'])
df4['G'] = df4['F'] - df4['E']


def test_time_index():
    assert time_index(df=df4) is True
    assert time_index(df=df3) is False


def test_check_dataframe():
    assert check_dataframe(df=df3) is True


def test_check_columns():
    assert check_columns(df, column_list=['A']) is True
    assert check_columns(df, column_list=['A','C']) is True
    assert check_columns(df, column_list=['A','B', 'C']) is True
    assert check_columns(df, column_list=['Z', 'B', 'C']) is False
    assert check_columns(df, column_list=['A', 'B','Z', 'C']) is False


def test_check_numeric():
    assert check_numeric(df=df, column_list=['A']) is True
    assert check_numeric(df=df, column_list=['A','B']) is True
    assert check_numeric(df=df, column_list=['C','D']) is False


def test_check_categorical():
    assert check_categorical(df=df, column_list=['C','D']) is True
    assert check_categorical(df=df, column_list=['C', 'D','E']) is True
    assert check_categorical(df=df, column_list=['C', 'D', 'E','A']) is False
    assert check_categorical(df=df, column_list=['A', 'B']) is False


def test_column_mean():
    assert isinstance(column_mean(df=df3,column_list=None), pd.Series)
    assert column_mean(df=df3)['A'] == 3.0
    assert isinstance(column_mean(df=df3,column_list=['B','C']), pd.Series)
    assert column_mean(df=df3,column_list=['B','C'])['B'] == 6.0
    assert 'A' not in column_mean(df=df3,column_list=['B','C']).index
    assert 'D' not in column_mean(df=df3,column_list=['B','C']).index


def test_get_column_types():
    assert isinstance(get_column_types(df=df3),dict)


def test_get_unique():
    assert len(get_unique(df=df,col_name='C')) == 3
    assert len(get_unique(df=df,col_name='A')) == 5
    assert get_unique(df=df, col_name='Z') is None


def test_unique_count():
    assert unique_count(df=df) == {'A': 5, 'B': 5, 'C': 3, 'D':2, 'E':2}


def test_extract_numeric_cols():
    assert isinstance(extract_numeric_cols(df=df), list)
    assert extract_numeric_cols(df=df) == ['A','B']


def test_extract_object_cols():
    assert extract_object_cols(df=df) == ['C']


def test_extract_datetime_cols():
    datetime_cols = extract_datetime_cols(df=df4)
    assert isinstance(datetime_cols, list)
    assert datetime_cols == ['E','F']


def test_extract_timedelta_cols():
    timedelta_cols = extract_timedelta_cols(df=df4)
    assert isinstance(timedelta_cols, list)
    assert timedelta_cols == ['G']


def test_extract_categorical_cols():
    assert extract_categorical_cols(df=df) == ['D']


def test_extract_bool_cols():
    assert extract_bool_cols(df=df) == ['E']


def test_extract_datetimetz_cols():
    datetime_cols = extract_datetimetz_cols(df=df4)
    assert isinstance(datetime_cols, list)
    assert len(datetime_cols) == 0


def test_extract_col_types():
    col_types = extract_col_types(df=df)
    assert 'numeric' in col_types.keys(), "col_types dictionary missing key numeric"
    assert 'object' in col_types.keys(), "col_types dictionary missing key object"
    assert 'boolean' in col_types.keys(), "col_types dictionary missing key boolean"
    assert 'categorical' in col_types.keys(), "col_types dictionary missing key categorical"
    assert 'datetime' in col_types.keys(), "col_types dictionary missing key datetime"
    assert 'timedelta' in col_types.keys(), "col_types dictionary missing key timedelta"


def test_calculate_correlation():
    assert isinstance(calculate_correlation(df=df, method='spearman').shape, tuple)


def test_combine_categorical_columns():
    col_types = {'numeric': ['A', 'B'],
                 'object': ['C'],
                 'boolean': [],
                 'categorical': ['D'],
                 'datetime': [],
                 'timedelta': []}

    col_types3 = extract_col_types(df=df3)

    assert combine_categorical_columns(df=df, col_types=col_types) == ['D','C']

    assert isinstance(combine_categorical_columns(df=df, col_types=col_types), list)
    assert isinstance(combine_categorical_columns(df=df3, col_types=col_types3), list)



