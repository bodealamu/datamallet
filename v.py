import plotly.express as px
from datamallet.visualization import AutoPlot
from datamallet.tabular.utils import combine_categorical_columns,extract_numeric_cols, get_unique, unique_count, extract_object_cols,extract_col_types, calculate_correlation
import pandas as pd


df = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':['dog','cat', 'sheep','dog','cat']})
df['D'] = ['male','male','male','female','female']
df['D'] = df['D'].astype('category')
print(df)
print(extract_numeric_cols(df))
print(get_unique(df=df, col_name='C'))
print(type(get_unique(df=df, col_name='D')))
print(unique_count(df=df))
print(extract_object_cols(df))
print('correlation')
print(calculate_correlation(df, method='pearson'))
print(calculate_correlation(df, method='pearson').shape)
print(type(calculate_correlation(df, method='pearson').shape))
print(extract_col_types(df=df))
xx =combine_categorical_columns(df=df, col_types=extract_col_types(df=df))
print(xx)
# tips = px.data.tips()
#
# autoplot = AutoPlot(df=tips)
# autoplot.plot()