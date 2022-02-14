from datamallet.visualization.plot import (create_box,
                                           create_pie,
                                           create_violin,
                                           create_histogram,
                                           create_correlation_plot,
                                           create_sunburst,
                                           create_treemap,
                                           create_density_chart,
                                           create_scatter,
                                           create_bar)
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

df3 = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':[2,3,4,5,6],
                   'D':[4,7,2,5,7],
                   })
col_type3 = extract_col_types(df=df3)


def test_create_pie():
    pie_charts_list = create_pie(df=df2,
                                 numeric_cols=['A','B','C','D'],
                                 list_of_categorical_columns=['E'],
                                 create_html=False,
                                 hole=False,
                                 filename='pie'
                                 )
    pie_charts_list2 = create_pie(df=df2,
                                  numeric_cols=['A','B','C','D'],
                                  list_of_categorical_columns=['E','F'],
                                  create_html=False,
                                  hole=False,
                                  filename='pie'
                                 )
    pie_charts_list3 = create_pie(df=df2,
                                  numeric_cols=['A','B','C','D'],
                                  list_of_categorical_columns=['A','B','C','D'],
                                  create_html=False,
                                  hole=False,
                                  filename='pie'
                                 )
    assert isinstance(pie_charts_list, list)
    assert isinstance(pie_charts_list2, list)
    assert isinstance(pie_charts_list3, list)
    assert isinstance(pie_charts_list[0], plotly.graph_objs.Figure)
    assert isinstance(pie_charts_list2[0], plotly.graph_objs.Figure)
    assert len(pie_charts_list3) == 0, "the columns provided as categorical are not all categorical"


def test_create_violin():
    violin_plots = create_violin(df=df2,
                                 col_types=col_type2,
                                 filename='violin',
                                 create_html=True,
                                 violinmode='group',
                                 points='all',
                                 display_box=True,
                                 color=None,
                                 maximum_number_violinplots=7 )

    violin_plots2 = create_violin(df=df3,
                                 col_types=col_type3,
                                 filename='violin',
                                 create_html=True,
                                 violinmode='group',
                                 points='all',
                                 display_box=True,
                                 color=None,
                                 maximum_number_violinplots=3)

    assert isinstance(violin_plots, list)
    assert isinstance(violin_plots[0], plotly.graph_objs.Figure)
    assert isinstance(violin_plots2, list)
    assert len(violin_plots2) == 0, "no chart created because there are no categorical columns"


def test_create_box():
    box_plots = create_box(df=df2,
                           col_types=col_type2,
                           points='outliers',
                           boxmode='group',
                           notched=False,
                           color=None,
                           filename='box',
                           create_html=False,
                           orientation='h'
                           )

    box_plots2 = create_box(df=df3,
                            col_types=col_type3,
                            points='outliers',
                            boxmode='group',
                            notched=False,
                            color=None,
                            filename='box',
                            create_html=False,
                            orientation='v'
                           )

    assert isinstance(box_plots, list)
    assert isinstance(box_plots[0], plotly.graph_objs.Figure)
    assert isinstance(box_plots2, list)
    assert len(box_plots2) == 0, "no chart created because there are no categorical columns"


def test_create_treemap():
    treemap_list = create_treemap(df=df2,
                                   col_types=col_type2,
                                   create_html=False,
                                   filename='treemap',
                                   limit=2)
    treemap_list3 = create_treemap(df=df3,
                                  col_types=col_type3,
                                  create_html=False,
                                  filename='treemap',
                                  limit=2)
    assert isinstance(treemap_list, list)
    assert isinstance(treemap_list3, list)
    assert len(treemap_list) != 0, 'an actual chart has been created'
    assert isinstance(treemap_list[0], plotly.graph_objs.Figure)
    assert len(treemap_list3) == 0,"no categorical variable, no chart created"


def test_create_sunburst():
    sunburst_list = create_sunburst(df=df2,
                                    col_types=col_type2,
                                    create_html=False,
                                    filename='sunburst',
                                    limit=2)
    sunburst_list3 = create_sunburst(df=df3,
                                     col_types=col_type3,
                                     create_html=False,
                                     filename='sunburst',
                                     limit=2)
    assert isinstance(sunburst_list, list)
    assert len(sunburst_list) != 0, 'an actual chart has been created'
    assert isinstance(sunburst_list[0], plotly.graph_objs.Figure)
    assert len(sunburst_list3) == 0,"no categorical variable, no chart created"


def test_create_correlation_plot():
    corr_plots = create_correlation_plot(df=c)
    corr_plots2 = create_correlation_plot(df=df2)
    assert isinstance(corr_plots, list)
    assert len(corr_plots) == 0
    assert isinstance(corr_plots2, list)
    assert isinstance(corr_plots2[0], plotly.graph_objs.Figure)


def test_create_histogram():
    histogram_list = create_histogram(df=df2,
                                      numeric_cols=['A','B','C','D'],
                                      nbins=20,
                                      marginal=None,
                                      cumulative=False,
                                      histnorm=None,
                                      filename='histogram',
                                      create_html=False)
    histogram_list2 = create_histogram(df=c,
                                      numeric_cols=[],
                                      nbins=20,
                                      marginal=None,
                                      cumulative=False,
                                      histnorm=None,
                                      filename='histogram',
                                      create_html=False)

    assert isinstance(histogram_list, list)
    assert isinstance(histogram_list2, list)
    assert isinstance(histogram_list[0], plotly.graph_objs.Figure)
    assert len(histogram_list2) == 0, "not numeric column"


def test_create_scatter():
    scatter_list = create_scatter(df=df2,
                                  col_types=extract_col_types(df2),
                                  filename='scatter',
                                  marginal_x=None,
                                  marginal_y=None,
                                  log_x=False,
                                  log_y=False,
                                  orientation='v',
                                  opacity=1.0,
                                  maximum_color_groups=5,
                                  create_html=False)
    scatter_list3 = create_scatter(df=df3,
                                   col_types=extract_col_types(df3),
                                   filename='scatter',
                                   marginal_x=None,
                                   marginal_y=None,
                                   log_x=False,
                                   log_y=False,
                                   orientation='v',
                                   opacity=1.0,
                                   maximum_color_groups=5,
                                   create_html=False)
    scatter_listc = create_scatter(df=c,
                                   col_types=extract_col_types(c),
                                   filename='scatter',
                                   marginal_x=None,
                                   marginal_y=None,
                                   log_x=False,
                                   log_y=False,
                                   orientation='v',
                                   opacity=1.0,
                                   maximum_color_groups=5,
                                   create_html=False)
    assert isinstance(scatter_list,list),'the output is expected to be a list of plotly graph objects'
    assert len(scatter_list) != 0, 'charts are created'
    assert isinstance(scatter_list[0], plotly.graph_objs.Figure)
    assert isinstance(scatter_list3,list),'the output is expected to be a list of plotly graph objects'
    assert len(scatter_list3) != 0, 'charts are created'
    assert isinstance(scatter_list3[0], plotly.graph_objs.Figure)
    assert isinstance(scatter_listc, list), 'the output is expected to be an empty list '
    assert len(scatter_listc) == 0, 'no charts are created because no numeric cols'


def test_create_density_chart():
    sample_df = pd.DataFrame({'A': [1, 2, 3, 4, 5],
                        'B': [2, 4, 6, 8, 10],
                        'C': [2, 3, 4, 5, 6],
                        'D': [4, 7, 2, 5, 7],
                        'E': [True, True, False, True, True],
                        })
    sample_df2 = pd.DataFrame({'A': [1, 2, 3, 4, 5],
                        'B': [2, 4, 6, 8, 10],
                        'C': [2, 3, 4, 5, 6],
                        'D': [4, 7, 2, 5, 7],
                        })

    col_type = extract_col_types(df=sample_df)
    col_type2 = extract_col_types(df=sample_df2)

    sample_charts = create_density_chart(df=sample_df,
                                         col_types=col_type,
                                         typr_of_chart='contour', create_html=False,
                                         filename='density_contour')
    sample_charts2 = create_density_chart(df=sample_df,
                                          col_types=col_type,
                                          typr_of_chart='heatmap', create_html=False,
                                          filename='density_contour')
    sample_charts3 = create_density_chart(df=sample_df2,
                                          col_types=col_type2,
                                          typr_of_chart='contour', create_html=False,
                                          filename='density_contour')
    sample_charts4 = create_density_chart(df=sample_df2,
                                          col_types=col_type2,
                                          typr_of_chart='heatmap', create_html=False,
                                          filename='density_contour')
    assert isinstance(sample_charts, list)
    assert isinstance(sample_charts[0], plotly.graph_objs.Figure)
    assert isinstance(sample_charts2, list)
    assert isinstance(sample_charts2[0], plotly.graph_objs.Figure)
    assert isinstance(sample_charts3, list)
    assert isinstance(sample_charts3[0], plotly.graph_objs.Figure)
    assert isinstance(sample_charts4, list)
    assert isinstance(sample_charts4[0], plotly.graph_objs.Figure)


def test_bar():
    fig_list = create_bar(df=df2,
                          col_types=extract_col_types(df=df2),
                          maximum_number_bars=10,
                          color='E',
                          opacity=1.0,
                          barmode='overlay',
                          filename='bars',
                          orientation='v',
                          width=None,
                          height=None,
                          log_x=False,
                          log_y=True,
                          create_html=True)
    assert len(fig_list) != 0








