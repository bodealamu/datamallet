from datamallet.tabular.preprocess import (ColumnDropper,
                                           ColumnRename)
import pandas as pd
df = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female'],
                   'E':[True,True,False,True,True]})


def test_column_dropper():
    column_dropper = ColumnDropper(column_list=['C','D','E'])
    droped_df = column_dropper.transform(X=df)

    assert 'A' in droped_df.columns
    assert 'B' in droped_df.columns


def test_column_rename():
    columnrenamer = ColumnRename(rename_dictionary={'A':'V',
                                                    'B':'W'})
    renamed_df = columnrenamer.transform(X=df)

    assert 'A' not in renamed_df.columns
    assert 'V' in renamed_df.columns
    assert 'B' not in renamed_df.columns
    assert 'W' in renamed_df.columns