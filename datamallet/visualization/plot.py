from .utils import (treemap_path,
                    create_pairs,
                    column_use,
                    figures_to_html)
from datamallet.tabular.utils import (check_dataframe,
                                      calculate_correlation)
import plotly.express as px


def create_pie(df,
               numeric_cols,
               pie_sector,
               create_html=False,
               hole=False,
               filename='pie'):
    """
    Creates a pie chart for every categorical variable in the dataset.
    :param df: pandas dataframe,
    :param numeric_cols: list of columns with numeric data
    :param pie_sector:list,
    :param create_html:boolean, whether the figures should be converted to HTML or not
    :param hole:boolean, hole in the pie chart
    :param filename:str, a suitable name for the produced html file, exclude the extension
    :return: list which contains graph objects
    """
    figure_list = list()

    for value in numeric_cols:
        for name in pie_sector:
            plot = px.pie(names=name,
                          data_frame=df,
                          values=value,
                          hole=hole,
                          title='Pie chart showing distribution of {} across {} segments'.format(value, name))

            figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_violin(df,
                  col_types,
                  filename='violin',
                  create_html=True,
                  violinmode='group',
                  points='all',
                  display_box=True,
                  color=None
                  ):
    """
    Creates a list of violin plot figure objects
    :param df: pandas dataframe
    :param col_types: dictionary that contains mapping of column type to list of column names
                    It is the output of extract_col_types in tabular module
    :param filename: str, filename for the html file
    :param create_html: boolean, whether to create an html file or not
    :param violinmode: str, how you want the charts to be displayed
    :param points: str, how the points in the violin chart should be displayed
    :param display_box: boolean, whether to display a box within the violin chart
    :param color:
    :return:
    """
    figure_list = list()

    column_use_dict = column_use(df, col_types=col_types, threshold=5)

    hue_cols = column_use_dict['hue']

    numeric_cols = col_types['numeric']

    if len(hue_cols) == 0:
        hue_cols.append(None)

    for col in numeric_cols:
        for hue in hue_cols:

            plot = px.violin(data_frame=df,
                             x=hue,
                             y=col,
                             points=points,
                             violinmode=violinmode,
                             box=display_box,
                             color=color,
                             title='Violinplot showing distribution of {} across {} categories'.format(col,hue))
            figure_list.append(plot)

    if create_html:

        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_box(df,
               col_types,
               points='outliers',
               boxmode='group',
               notched=False,
               color=None,
               filename='box',
               create_html=True
               ):
    """
    Creates a list of boxplot figure objects created for the entire dataset
    :param df: pandas dataframe
    :param col_types: dictionary that contains mapping of column type to list of column names
                    It is the output of extract_col_types in tabular module
    :param points:str, whether to show the points in a box plot possible options are 'outliers', 'all',False, 'suspectedoutliers'
    :param boxmode: str, how to display the boxes in a boxplot.
                    Options are 'group' or 'overlay'. In group mode,
                    boxes are placed beside each other, in overlay mode,
                    boxes are placed on top of each other.
    :param notched: boolean, True or False, boxes are drawn with notches
    :param color:
    :param filename:
    :param create_html:boolean, whether to create an html file or not
    :return:
    """
    figure_list = list()
    numeric_cols = col_types['numeric']

    column_use_dict = column_use(df, col_types=col_types, threshold=5)

    hue_cols = column_use_dict['hue']
    if len(hue_cols) == 0:
        hue_cols.append(None)

    for col in numeric_cols:
        for hue in hue_cols:

            plot = px.box(data_frame=df,
                          x=hue,
                          y=col,
                          points=points,
                          boxmode=boxmode,
                          notched=notched,
                          color=color,
                          title='Boxplot showing distribution of {} across {} categories'.format(col,hue)
                          )
            figure_list.append(plot)

    if create_html:

        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_treemap(df,
                   numeric_cols,
                   create_html=True,
                   filename='treemap',
                   limit=2
                   ):
    """

    :param df:pandas dataframe
    :param numeric_cols:list of column names of numeric columns
    :param create_html: boolean, whether to create an html file or not
    :param filename:
    :param limit:int, maximum path depth
    :return:
    """
    figure_list = list()

    path_list = treemap_path(df=df, limit=limit)

    for col in numeric_cols:

        plot = px.treemap(data_frame=df,
                          path=path_list,
                          values=col,
                          title='Treemap of {} across paths {}'.format(col, str(path_list))
                          )

        figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_sunburst(df,
                    numeric_cols,
                    create_html=True,
                    filename='sunburst',
                    limit=2
                    ):
    """

    :param df:
    :param numeric_cols:list of column names of numeric columns
    :param create_html: boolean, whether to create an html file or not
    :param filename:
    :param limit:int, maximum path depth
    :return:
    """
    figure_list = list()

    path_list = treemap_path(df=df, limit=limit)

    for col in numeric_cols:

        plot = px.sunburst(data_frame=df,
                           path=path_list,
                           values=col,
                           title='Sunburst chart of {} across paths {}'.format(col, str(path_list))
                           )

        figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_correlation_plot(df, correlation_method='pearson'):
    """
    Creates a correlation plot for the provided dataframe
    based on the correlation method supplied and returns a list of plotly graph objects
    :param df: pandas dataframe
    :param correlation_method: str, method for computing correlation, one of kendall, pearson, spearman
    :return: list of graph objects
    """
    figure_list = list()
    check = check_dataframe(df=df)
    available_method = correlation_method in ['pearson', 'kendall', 'spearman']

    if check and available_method:

        correlation = calculate_correlation(df=df, method=correlation_method)

        plot = px.imshow(img=correlation,
                         title='Correlation plot using {} method'.format(correlation_method))

        figure_list.append(plot)

    return figure_list


def create_histogram(df,
                     numeric_cols,
                     nbins=None,
                     marginal=None,
                     cumulative=False,
                     histfunc=None,
                     histnorm=None,
                     filename='histogram',
                     create_html=True
                     ):
    """

    :param df:
    :param numeric_cols:
    :param nbins:
    :param marginal:
    :param cumulative:
    :param histfunc:
    :param histnorm:
    :param filename:
    :param create_html: boolean, whether to create an html file or not
    :return:
    """

    figure_list = list()

    for col in numeric_cols:
        plot = px.histogram(data_frame=df,
                            nbins=nbins,
                            x=col,
                            marginal=marginal,
                            cumulative=cumulative,
                            histfunc=histfunc,
                            histnorm=histnorm,
                            title='Distribution of {}'.format(col)
                            )
        figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_scatter(df,
                   col_types,
                   basic=True,
                   filename='scatter',
                   marginal_x=None,
                   marginal_y=None,
                   log_x=False,
                   log_y=False,
                   create_html=True):
    """

    :param df:
    :param col_types: dictionary that contains mapping of column type to list of column names
                    It is the output of extract_col_types in tabular module
    :param basic:boolean, whether to create a basic scatterplot or not
    :param filename:
    :param marginal_x:options for including marginal charts on x axis
    :param marginal_y:options for including marginal charts on y axis
    :param log_x:boolean, whether to create a log axis
    :param log_y:boolean, whether to create a log axis
    :param create_html: boolean, whether to create an html file or not
    :return:
    """
    numeric_cols = col_types['numeric']
    plot_pairs = create_pairs(df, numeric_cols=numeric_cols)

    figure_list = list()

    if basic:
        for pair in plot_pairs:
            x,y = pair
            plot = px.scatter(data_frame=df,
                              x=x,
                              y=y,
                              log_y=log_y,
                              log_x=log_x,
                              marginal_x=marginal_x,
                              marginal_y=marginal_y,
                              title='Plot of {} vs {}'.format(x,y))
            figure_list.append(plot)

    else:
        cols_use_dict = column_use(df, col_types=col_types, threshold=5)
        name_list = cols_use_dict['name']
        hue_list = cols_use_dict['hue']

        if len(name_list) == 0:
            name_list.append(None)

        if len(hue_list) == 0:
            hue_list.append(None)

        for pair in plot_pairs:
            x,y = pair
            for names in name_list:
                for hue in hue_list:
                    plot = px.scatter(data_frame=df,
                                      x=x,
                                      y=y,
                                      color=hue,
                                      log_y=log_y,
                                      log_x=log_x,
                                      marginal_x=marginal_x,
                                      marginal_y=marginal_y,
                                      hover_name=names,
                                      title='Plot of {} vs {} with color {} and hover name {}'.format(x, y, hue,names))

                    figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list












