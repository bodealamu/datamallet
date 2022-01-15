from datamallet.tabular.preprocess import (ColumnDropper,
                                           NaFiller,
                                           DropPercentageMissing,
                                           NADropper,
                                           ConstantValueFiller,
                                           ColumnRename)
import pandas as pd
import numpy as np

df = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female'],
                   'E':[True,True,False,True,True]})

df2 = pd.DataFrame({'A':[np.nan,2,3,4,5,8],
                   'B':[2,np.nan,np.nan,np.nan,10,9],
                   'C':[1,3,5, np.nan, np.nan,7]})

d = pd.DataFrame({'A':[np.nan,2,3,4,5,8],
                   'B':[2,np.nan,np.nan,np.nan,10,9],
                   'C':[1,3,5, np.nan, np.nan,7],
                   'D':[4,np.nan,np.nan, np.nan, np.nan,7]})

df3 = pd.DataFrame({'A':[np.nan,2,3,4,5],
                   'B':[2,np.nan,np.nan,np.nan,10],
                   'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female'],
                   'E':[True,True,False,True,True]})


def test_column_dropper():
    column_dropper = ColumnDropper(column_list=['C','D','E'])
    dropped_df = column_dropper.transform(X=df)

    assert 'A' in dropped_df.columns
    assert 'B' in dropped_df.columns
    assert 'C' not in dropped_df.columns
    assert 'D' not in dropped_df.columns
    assert 'E' not in dropped_df.columns


def test_NaFiller():
    nafiller = NaFiller( method='bfill',limit=None,column_list=None)
    cx = nafiller.transform(X=df2)
    assert cx['B'].mean() == 8.5
    assert cx['A'].mean() == 4.0
    assert cx['C'].mean() == 5.0
    nafiller = NaFiller( method='ffill',limit=None,column_list=None)
    cx = nafiller.transform(X=df2)
    assert cx['B'].mean() == 4.5
    assert cx['A'].mean() == 4.4
    assert round(cx['C'].mean(),2) == 4.33
    nafiller = NaFiller( method='mean',limit=None,column_list=None)
    cx = nafiller.transform(X=df2)
    assert cx['B'].mean() == 7.0
    assert round(cx['A'].mean(),2) == 4.4
    assert cx['C'].mean() == 4.0
    nafiller = NaFiller(method='mean', column_list=['B', 'C'], limit=1)
    cx = nafiller.transform(X=d)
    assert cx['B'].mean() == 7.0
    assert cx['A'].mean() == 4.4
    assert cx['C'].mean() == 4.0
    assert cx['D'].mean() == 5.5
    nafiller = NaFiller(method='bfill', column_list=['C', 'D'], limit=1)
    cx = nafiller.transform(X=d)
    assert cx['B'].mean() == 7.0
    assert cx['A'].mean() == 4.4
    assert cx['C'].mean() == 4.6
    assert cx['D'].mean() == 6.0
    nafiller = NaFiller(method='ffill', column_list=['C', 'D'], limit=1)
    cx = nafiller.transform(X=d)
    assert cx['B'].mean() == 7.0
    assert cx['A'].mean() == 4.4
    assert cx['C'].mean() == 4.2
    assert cx['D'].mean() == 5.0


def test_constantvaluefiller():
    df2 = pd.DataFrame({'A': [np.nan, 2, 3, 4, 5, 8], 'B': [2, np.nan, np.nan, np.nan, 10, 9],
                        'C': [1, 3, 5, np.nan, np.nan, 7]})
    cvf = ConstantValueFiller(value={'A': 100, 'B': 200, 'C': 300}, limit=1)
    vx = cvf.transform(X=df2)
    assert vx['A'].sum() == 122
    cvf = ConstantValueFiller(value={'A': 100, 'B': 200, 'C': 300}, limit=None)
    vx = cvf.transform(X=df2)
    assert vx['C'].sum() == 616
    assert vx['A'].sum() == 122
    cvf = ConstantValueFiller(value=10, limit=None)
    vx = cvf.transform(X=df2)
    assert vx['C'].sum() == 36
    assert vx['A'].sum() == 32


def test_column_rename():
    columnrenamer = ColumnRename(rename_dictionary={'A':'V',
                                                    'B':'W'})
    renamed_df = columnrenamer.transform(X=df)

    assert 'A' not in renamed_df.columns
    assert 'V' in renamed_df.columns
    assert 'B' not in renamed_df.columns
    assert 'W' in renamed_df.columns
    assert 'C' in renamed_df.columns
    assert 'D' in renamed_df.columns
    assert 'E' in renamed_df.columns


def test_nadropper():
    nadropper = NADropper(axis='columns', how='any')
    droped2 = nadropper.transform(X=df2)
    assert 'A' not in droped2.columns
    assert 'B' not in droped2.columns
    nadropper = NADropper(axis='columns', how='all')
    droped = nadropper.transform(X=df2)
    assert 'A' in droped.columns
    assert 'B' in droped.columns
    nadropper = NADropper(axis='index', how='any', )
    d = nadropper.transform(X=df2)
    assert len(d) == 1


def test_dropPercentageMissing():
    bn = DropPercentageMissing(threshold=20).transform(X=df)

    assert 'toy' not in bn.columns



