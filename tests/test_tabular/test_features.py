from datamallet.tabular.feature import (ColumnAdder,)
import pandas as pd

df = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female'],
                   'E':[True,True,False,True,True]})


def test_column_adder():
    column_adder = ColumnAdder(column_list=['A','B'],new_column_name='Z')
    added_df = column_adder.transform(X=df)

    assert 'Z' in added_df.columns
    assert added_df['A'].sum() + added_df['B'].sum() == added_df['Z'].sum()

