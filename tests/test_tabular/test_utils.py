from datamallet.tabular.utils import (extract_numeric_cols,
                                      check_columns,
                                      get_unique,extract_col_types,
                                      unique_count,
                                      extract_object_cols,
                                      extract_categorical_cols,
                                      extract_bool_cols,
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


def test_extract_numeric_cols():
    assert isinstance(extract_numeric_cols(df=df), list)
    assert extract_numeric_cols(df=df) == ['A','B']


def test_check_columns():
    assert check_columns(df, column_list=['A']) is True
    assert check_columns(df, column_list=['A','C']) is True
    assert check_columns(df, column_list=['A','B', 'C']) is True
    assert check_columns(df, column_list=['Z', 'B', 'C']) is False


def test_get_unique():
    assert len(get_unique(df=df,col_name='C')) == 3
    assert len(get_unique(df=df,col_name='A')) == 5
    assert get_unique(df=df, col_name='Z') is None


def test_unique_count():
    assert unique_count(df=df) == {'A': 5, 'B': 5, 'C': 3, 'D':2, 'E':2}


def test_extract_object_cols():
    assert extract_object_cols(df=df) == ['C']


def test_extract_categorical_cols():
    assert extract_categorical_cols(df=df) == ['D']


def test_extract_bool_cols():
    assert extract_bool_cols(df=df) == ['E']


def test_calculate_correlation():
    assert isinstance(calculate_correlation(df=df, method='spearman').shape, tuple)


def test_get_column_types():
    assert isinstance(get_column_types(df=df), dict)


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


def test_check_numeric():
    assert check_numeric(df=df, column_list=['A']) is True
    assert check_numeric(df=df, column_list=['A','B']) is True
    assert check_numeric(df=df, column_list=['C','D']) is False
