from datamallet.tabular.utils import (extract_numeric_cols,
                                      extract_col_types,
                                      get_unique,
                                      check_dataframe,
                                      unique_count,
                                      calculate_correlation)
import plotly.express as px
import pandas as pd


def pie_sectors(df, maximum_number_sectors=3):
    """
    Determines columns in a dataframe whose unique value count is
    less than or equal to the maximum number of sectors
    :param df:
    :param maximum_number_sectors:int,
    :return:
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(maximum_number_sectors, int), "maximum_number_sectors must be an integer"

    columns_list = list()
    unique_count_dict = unique_count(df=df)

    for column, count in unique_count_dict.items():
        if count <= maximum_number_sectors:
            columns_list.append(column)

    return columns_list


def __combine_object_categorical(df):
    """
    Combined columns of types categorical, object, and boolean into a list
    :param df: pandas dataframe
    :return:
    """

    combined = list()

    if check_dataframe(df=df):
        col_types = extract_col_types(df=df)

        categorical = col_types['categorical']
        object_cols = col_types['object']
        boolean_cols = col_types['boolean']

        combined.extend(categorical)
        combined.extend(object_cols)
        combined.extend(boolean_cols)

    return combined


def column_use(df, threshold=5):
    """
    This function helps in determining whether a column in a dataframe
       should be used to color the data points in a chart or if it is
        okay for simply naming the points
    :param df: pandas dataframe
    :param threshold: int, think of it as the number
           of distinct colors in a chart(e.g scatterplot)
    :return:
    """
    all_categorical_cols = __combine_object_categorical(df=df)

    number_of_rows = df.shape[0]

    column_use_dict = dict()
    names_list = list()
    hue_list = list()

    for col in all_categorical_cols:
        number_of_unique = len(get_unique(df=df, col_name=col))
        ratio = number_of_rows / number_of_unique

        if ratio < threshold:
            names_list.append(col)

        else:
            hue_list.append(col)

    column_use_dict['name'] = names_list
    column_use_dict['hue'] = hue_list

    return column_use_dict


def figures_to_html(figs, filename):
    """
    Utility function that creates a single html file when given the list of plotly graph objects
    :param figs: python list of plotly graph objects
    :param filename: str, string nmae for file excluding any extension
    :return: None
    """
    assert isinstance(figs, list), "figs is expected to be a list of plotly graph objects"
    assert isinstance(filename, str), "filename must be a string"
    html_filename = filename+'.html'

    with open(html_filename, 'a') as f:
        for fig in figs:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    return None


def __create_pairs(df):
    """
    Create a non repeat list of tuples which contains pairs of
    numeric cols in df for visualization purpose as x and y axis
    :param df: pandas dataframe
    :return: list of tuple of non repeat pairing
    """

    numeric_cols = extract_numeric_cols(df=df)
    passed_cols = set()
    pairs = list()

    for col1 in numeric_cols:
        for col2 in numeric_cols:
            if col1 == col2:
                continue

            if len(passed_cols) == 0 or col2 not in passed_cols:
                pairs.append((col1,col2))

        passed_cols.add(col1)

    return pairs


def treemap_path(df, limit=3):
    """
    It helps to determine the path for a tree map or sunburst chart,
    the idea is to start the path from the column with the
    least number of unique values to the one with the most
    :param df: pandas dataframe
    :param limit: the number of elements in the path list,
                i.e maximum number of treemap/sunburst categories
    :return:
    """
    check = check_dataframe(df=df)
    col_list = list()
    sorted_cols = None

    if check:
        column_type = extract_col_types(df)

        col_list.extend(column_type['object'])
        col_list.extend(column_type['boolean'])
        col_list.extend(column_type['categorical'])

        unique_counts = [len(get_unique(df=df,col_name=x)) for x in col_list]

        sorted_columns = [col_name for _,col_name in sorted(zip(unique_counts, col_list))]

        sorted_cols = sorted_columns[:limit]

    return sorted_cols


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
    :return:
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
                  numeric_cols,
                  filename='violin',
                  create_html=True,
                  violinmode='group',
                  points='all',
                  display_box=True,
                  color=None
                  ):
    figure_list = list()

    column_use_dict = column_use(df,threshold=5)

    hue_cols = column_use_dict['hue']

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
               numeric_cols,
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
    :param numeric_cols: list, list of column names which have numeric data type
    :param points:str, whether to show the points in a box plot possible options are 'outliers', 'all',False, 'suspectedoutliers'
    :param boxmode: str, how to display the boxes in a boxplot.
                    Options are 'group' or 'overlay'. In group mode,
                    boxes are placed beside each other, in overlay mode,
                    boxes are placed on top of each other.
    :param notched: boolean, True or False, boxes are drawn with notches
    :param color:
    :param filename:
    :param create_html:
    :return:
    """
    figure_list = list()

    column_use_dict = column_use(df,threshold=5)

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


def create_sunburst(df,numeric_cols,
                    create_html=True,
                    filename='sunburst',
                    limit=2
                    ):
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


def create_scatter(df, basic=True,
                   filename='scatter',
                   marginal_x=None,
                   marginal_y=None,
                   log_x=False,
                   log_y=False,
                   create_html=True):
    plot_pairs = __create_pairs(df)

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
        cols_use_dict = column_use(df, threshold=5)
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















