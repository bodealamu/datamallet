from datamallet.visualization.utils import (pie_sectors,
                                            create_pairs,
                                            treemap_path)
from datamallet.tabular.utils import extract_col_types, combine_categorical_columns
import pandas as pd

df = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female'],
                   'E':[True,True,False,True,True],
                   'F':['chess', 'scrabble','checkers', 'card games', 'dominoes']})


def test_pie_sectors():
    column_list = pie_sectors(df, maximum_number_sectors=3)
    assert 'C' in column_list
    assert 'D' in column_list
    assert 'E' in column_list
    assert 'F' not in column_list, "the number of unique items in column F exceeds the maximum"
