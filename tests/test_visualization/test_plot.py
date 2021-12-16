from datamallet.visualization.plot import (create_box,
                                           create_pie,
                                           create_violin,
                                           create_histogram,
                                           create_correlation_plot,
                                           create_sunburst,
                                           create_treemap,
                                           create_scatter)
from datamallet.tabular.utils import extract_col_types
import pandas as pd
import plotly

df2 = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':[2,3,4,5,6],
                   'D':[4,7,2,5,7],
                   'E':[True,True,False,True,True],
                   'F':['chess', 'scrabble','checkers', 'card games', 'dominoes']})

col_type2 = extract_col_types(df=df2)

c = pd.DataFrame({'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female'],
                   'F':['chess', 'scrabble','checkers', 'card games', 'dominoes']})


def test_create_box():
    box_plots = create_box(df=df2,
                           col_types=col_type2,
                           points='outliers',
                           boxmode='group',
                           notched=False,
                           color=None,
                           filename='box',
                           create_html=False
                           )

    assert isinstance(box_plots, list)


def test_create_pie():
    pie_charts_list = create_pie(df=df2,
                                 numeric_cols=['A','B','C','D'],
                                 list_of_categorical_columns=['E'],
                                 create_html=False,
                                 hole=False,
                                 filename='pie'
                                 )
    assert isinstance(pie_charts_list, list)
    assert isinstance(pie_charts_list[0], plotly.graph_objs.Figure)


def test_create_histogram():
    histogram_list = create_histogram(df=df2,
                                      numeric_cols=['A','B','C','D'],
                                      nbins=None,
                                      marginal=None,
                                      cumulative=False,
                                      histfunc=None,
                                      histnorm=None,
                                      filename='histogram',
                                      create_html=False)

    assert isinstance(histogram_list, list)
    assert isinstance(histogram_list[0], plotly.graph_objs.Figure)


def test_create_correlation_plot():
    corr_plots = create_correlation_plot(df=c)
    assert isinstance(corr_plots, list)
    assert len(corr_plots) == 0