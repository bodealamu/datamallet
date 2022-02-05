from datamallet.tabular.feature import (ColumnAdder,
                                        ExpandingTransformer,
                                        ColumnMultiplier,
                                        GroupbyTransformer,
                                        SimpleEncoder,
                                        ColumnSubtraction)
import pandas as pd
import numpy as np

df = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female'],
                   'E':[True,True,False,True,True]})

df2 = pd.DataFrame({'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female']})

df3 = pd.DataFrame({'A':[1,1,2,1,1],
                   'B':[2,2,1,2,0],})

df4 = pd.DataFrame({'Age':[1,2,3,4,5],
                   'Gender':['Male','Female','Unknown','Male','Female'],
                    'City':['austin', 'austin', 'lagos','abuja', 'ibadan']
                   })


def test_column_adder():
    column_adder = ColumnAdder(column_list=['A','B'],new_column_name='Z')
    added_df = column_adder.transform(X=df)
    non_added = ColumnAdder(column_list=['C','D'],new_column_name='W').transform(X=df2)

    assert 'Z' in added_df.columns
    assert added_df['A'].sum() + added_df['B'].sum() == added_df['Z'].sum()
    assert 'W' not in non_added.columns # ColumnAdder wont work for text columns


def test_column_multiplier():
    multiplied_df = ColumnMultiplier(column_list=['A','B'], new_column_name='Z').transform(X=df3)

    assert 'Z' in multiplied_df.columns
    assert multiplied_df['Z'].sum() == 8


def test_column_substraction():
    subtracted_df = ColumnSubtraction(left='A', right='B', new_column_name='C').transform(df3)
    assert 'C' in subtracted_df.columns
    assert subtracted_df['C'].sum() == -1


def test_expandingtransformer():
    df = pd.DataFrame({"B": [0, 1, 2, np.nan, 4]})
    expander = ExpandingTransformer(column_list=['B'],
                                    min_periods=2,
                                    aggregation_function='sum')

    df_new = expander.transform(X=df)

    df2= pd.DataFrame({"B": [0, 1, 2, np.nan, 4],
                       "A": [0, 1, 0, np.nan, 4]})
    expander = ExpandingTransformer(column_list=['B'],
                                    min_periods=2,
                                    aggregation_function='sum')

    df_new2 = expander.transform(X=df2)

    assert df_new2['B'].sum() == 14.0
    assert df_new['B'].sum() == 14.0
    assert df['B'].sum() == 7.0
    assert df2['A'].sum() == df_new2['A'].sum()
    assert isinstance(df_new2, pd.DataFrame)
    assert isinstance(df_new, pd.DataFrame)


def test_groupbytransformer():
    grouped_df = GroupbyTransformer(column_list=['Gender', 'City'], aggregation_method='mean').transform(df4)
    assert grouped_df['Age']['Female']['austin'] == 2.0
    grouped_df = GroupbyTransformer(column_list=['City'], aggregation_method='mean').transform(df4)
    assert grouped_df['Age']['abuja'] == 4.0


def test_SimpleEncoder():
    df = pd.DataFrame({'A': ['a', 'b', 'a'], 'B': ['b', 'a', 'c'],
                       'C': [1, 2, 3]})
    encoded_df = SimpleEncoder().transform(X=df)
    assert 'B_c' in encoded_df.columns





