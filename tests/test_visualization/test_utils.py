from datamallet.visualization.utils import (pie_sectors,
                                            create_pairs,
                                            treemap_path)
from datamallet.tabular.utils import extract_col_types, combine_categorical_columns
import pandas as pd

df = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female'],
                   'E':[True,True,False,True,True]})

df['D'] = df['D'].astype('category')


