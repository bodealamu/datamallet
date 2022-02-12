from .utils import (hierarchical_path, columns_with_distinct_values,
                    create_pairs,
                    figures_to_html)
from datamallet.tabular.utils import (check_categorical,
                                      check_numeric,
                                      extract_numeric_cols,
                                      calculate_correlation)
import pandas as pd
import plotly.express as px


def create_pie(df,
               numeric_cols,
               list_of_categorical_columns,
               create_html=False,
               width=None,
               height=None,
               opacity=1.0,
               hole=False,
               filename='pie'):
    """
    Creates a pie chart for every categorical variable in the dataset.
    :param df: pandas dataframe,
    :param numeric_cols: list of columns with numeric data
    :param list_of_categorical_columns:list of column names which have categorical data.
            Output of function columns_with_distinct_values(df=self.df, categorical_only=True,
                                                        maximum_number_distinct_values=maximum_number_sectors)
            Also output of extract_categorical_cols in tabular/utils module
    :param create_html:boolean, whether the figures should be converted to HTML or not
    :param opacity: float, Value between 0 and 1. Sets the opacity for markers
    :param hole:boolean, hole in the pie chart
    :param filename:str, a suitable name for the produced html file, exclude the extension
    :return: list which contains plotly graph objects
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(numeric_cols, list), "numeric_cols must be a list"
    assert isinstance(list_of_categorical_columns, list), "list_of_categorical_columns must be a list"
    assert len(list_of_categorical_columns) != 0, "list_of_categorical_columns must not be empty"
    assert len(numeric_cols) != 0, "numeric_cols must not be empty"
    assert isinstance(create_html, bool), "create_html must be a boolean"
    assert isinstance(opacity,float),"opacity must be a float"
    assert opacity <= 1.0, "opacity must be a number between 0 and 1"
    assert opacity >= 0.0, "opacity must be a number between 0 and 1"
    assert isinstance(hole, bool), "hole must be a boolean"
    assert isinstance(filename, str), "filename must be a string without a dot or an extension"
    assert '.' not in filename, "filename doesn't need an extension"
    assert isinstance(width, int) or width is None
    assert isinstance(height, int) or height is None

    figure_list = list()

    if check_numeric(df=df,column_list=numeric_cols) and check_categorical(df=df,
                                                                           column_list=list_of_categorical_columns):

        for value in numeric_cols:
            for name in list_of_categorical_columns:
                plot = px.pie(names=name,
                              data_frame=df,
                              values=value,width=width, height=height,
                              hole=hole,
                              title='Pie chart showing distribution of {} across {} segments'.format(value, name))

                figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_violin(df,
                  col_types,
                  filename='violin',
                  width=None,
                  height=None,
                  create_html=True,
                  violinmode='group',
                  points='all',
                  display_box=True,
                  color=None,
                  maximum_number_violinplots=7
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
    :param maximum_number_violinplots:
    :return:list which contains plotly graph objects
    """
    assert isinstance(df,pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(col_types, dict), "col_types must be a dictionary"
    assert isinstance(create_html, bool), "create_html must be a boolean"
    assert isinstance(violinmode,str), "violinmode must be a string"
    assert isinstance(points,str), "points must be a string"
    assert isinstance(display_box,bool), "display_box must be a boolean"
    assert isinstance(maximum_number_violinplots, int), "maximum_number_violinplots must be an integer"
    assert isinstance(filename, str), "filename must be a string with a dot or an extension"
    assert color in col_types['categorical'] or color in col_types['boolean'] or color in col_types['object'] or color is None
    keys = col_types.keys()
    assert 'numeric' in keys, "col_types dictionary missing key numeric"
    assert 'object' in keys, "col_types dictionary missing key object"
    assert 'boolean' in keys, "col_types dictionary missing key boolean"
    assert 'categorical' in keys, "col_types dictionary missing key categorical"
    assert 'datetime' in keys, "col_types dictionary missing key datetime"
    assert 'timedelta' in keys, "col_types dictionary missing key timedelta"
    assert violinmode in ['group', 'overlay'],"violinmode must be either group or overlay"
    assert points in ['all', 'outliers', 'suspectedoutliers', False],"accepted values for points 'all', 'outliers', " \
                                                                     "'suspectedoutliers'"
    assert '.' not in filename, "filename doesn't need an extension"
    assert isinstance(width, int) or width is None
    assert isinstance(height, int) or height is None

    figure_list = list()

    numeric_cols = col_types['numeric']

    categorical_columns = columns_with_distinct_values(df=df,
                                                       maximum_number_distinct_values=maximum_number_violinplots)

    if len(numeric_cols) != 0 and len(categorical_columns) != 0:
        for col in numeric_cols:
            for category in categorical_columns:

                plot = px.violin(data_frame=df,
                                 x=category,
                                 y=col,width=width, height=height,
                                 points=points,
                                 violinmode=violinmode,
                                 box=display_box,
                                 color=color,
                                 title='Violinplot showing distribution of {} across {} categories'.format(col,category))
                figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_box(df,
               col_types,
               points='outliers',
               boxmode='group',
               width=None,
               height=None,
               notched=False,
               color=None,
               filename='box',
               create_html=True,
               maximum_number_boxplots=7,
               orientation='v'
               ):
    """
    Creates a list of boxplot figure objects created for the entire dataset
    :param df: pandas dataframe
    :param col_types: dictionary that contains mapping of column type to list of column names
                    It is the output of extract_col_types in tabular module
    :param points:str, whether to show the points in a box plot possible options are 'outliers', 'all',False,
                 'suspectedoutliers'
    :param boxmode: str, how to display the boxes in a boxplot.
                    Options are 'group' or 'overlay'. In group mode,
                    boxes are placed beside each other, in overlay mode,
                    boxes are placed on top of each other.
    :param notched: boolean, True or False, boxes are drawn with notches
    :param color:
    :param filename::str, filename for the html file
    :param create_html:boolean, whether to create an html file or not
    :param maximum_number_boxplots: int,
    :param orientation: str, how the plot should be orientated, 'v' for vertical, 'h' for horizontal
    :return:list which contains plotly graph objects
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(col_types, dict), "col_types must be a dictionary with column " \
                                        "name as keys and column type as value"
    keys = col_types.keys()
    assert 'numeric' in keys, "col_types dictionary missing key numeric"
    assert 'object' in keys, "col_types dictionary missing key object"
    assert 'boolean' in keys, "col_types dictionary missing key boolean"
    assert 'categorical' in keys, "col_types dictionary missing key categorical"
    assert 'datetime' in keys, "col_types dictionary missing key datetime"
    assert 'timedelta' in keys, "col_types dictionary missing key timedelta"
    assert isinstance(points, str), "points must be a string"
    assert points in ['all', 'outliers', 'suspectedoutliers', False],"accepted values for points 'all', " \
                                                                     "'outliers', " \
                                                                     "'suspectedoutliers'"
    assert isinstance(boxmode, str), "boxmode must be a string"
    assert boxmode in ['group', 'overlay'], "boxmode must be either group or overlay"
    assert isinstance(notched, bool), "notched must be a boolean"
    assert isinstance(create_html,bool), "create_html must be a boolean"
    assert isinstance(maximum_number_boxplots,int), "maximum_number_boxplots must be an integer"
    assert isinstance(filename, str), "filename must be a string with a dot or an extension"
    assert '.' not in filename, "filename doesn't need an extension"
    assert isinstance(orientation,str), "orientation must be a string"
    assert orientation in ['v','h'], "options for orientation are 'v' or 'h' "
    assert isinstance(width, int) or width is None
    assert isinstance(height, int) or height is None

    figure_list = list()
    numeric_cols = col_types['numeric']

    categorical_columns = columns_with_distinct_values(df=df,
                                                       maximum_number_distinct_values=maximum_number_boxplots)

    if len(numeric_cols) != 0 and len(categorical_columns) != 0:

        for col in numeric_cols:
            for category in categorical_columns:

                plot = px.box(data_frame=df,
                              x=category,
                              y=col,width=width, height=height,
                              points=points,
                              boxmode=boxmode,
                              notched=notched,
                              color=color,
                              orientation=orientation,
                              title='Boxplot showing distribution of {} across {} categories'.format(col,category)
                              )
                figure_list.append(plot)

    if create_html:

        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_treemap(df,
                   col_types,
                   create_html=True,
                   color=None,
                   width=None,
                   height=None,
                   filename='treemap',
                   limit=2
                   ):
    """

    :param df:pandas dataframe
    :param col_types: dictionary that contains mapping of column type to list of column names
                    It is the output of extract_col_types in tabular module
    :param create_html: boolean, whether to create an html file or not
    :param color: str, column name to use for color
    :param filename::str, filename for the html file
    :param limit:int, maximum path depth
    :return:list which contains plotly graph objects
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(create_html, bool),"create_html must be a boolean"
    assert isinstance(limit, int),"limit must be a int"
    assert limit > 1, "limit must be at least 2, to have a meaningful hierarchical chart"
    assert isinstance(filename, str), "filename must be a string with a dot or an extension"
    assert isinstance(col_types, dict), "col_types must be a dictionary"
    keys = col_types.keys()
    assert 'numeric' in keys, "col_types dictionary missing key numeric"
    assert 'object' in keys, "col_types dictionary missing key object"
    assert 'boolean' in keys, "col_types dictionary missing key boolean"
    assert 'categorical' in keys, "col_types dictionary missing key categorical"
    assert 'datetime' in keys, "col_types dictionary missing key datetime"
    assert 'timedelta' in keys, "col_types dictionary missing key timedelta"
    assert '.' not in filename, "filename doesn't need an extension"
    assert isinstance(width, int) or width is None
    assert isinstance(height, int) or height is None

    figure_list = list()

    path_list = hierarchical_path(df=df, limit=limit, col_types=col_types)

    numeric_cols = col_types['numeric']

    if len(path_list) > 1:
        for col in numeric_cols:

            plot = px.treemap(data_frame=df,
                              path=path_list,
                              color=color,
                              values=col,width=width, height=height,
                              title='Treemap of {} across paths {}'.format(col, str(path_list))
                              )

            figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_sunburst(df,
                    col_types,
                    color=None,
                    width=None,
                    height=None,
                    create_html=True,
                    filename='sunburst',
                    limit=2
                    ):
    """

    :param df:
    :param col_types: dictionary that contains mapping of column type to list of column names
                    It is the output of extract_col_types in tabular module
    :param create_html: boolean, whether to create an html file or not
    :param color: str, column name to color the chart
    :param filename::str, filename for the html file
    :param limit:int, maximum path depth
    :return:list which contains plotly graph objects
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(create_html, bool),"create_html must be a boolean"
    assert isinstance(limit, int),"limit must be a int"
    assert limit > 1, "limit must be at least 2, to have a meaningful hierarchical chart"
    assert isinstance(filename, str), "filename must be a string with a dot or an extension"
    assert isinstance(col_types, dict), "col_types must be a dictionary"
    keys = col_types.keys()
    assert 'numeric' in keys, "col_types dictionary missing key numeric"
    assert 'object' in keys, "col_types dictionary missing key object"
    assert 'boolean' in keys, "col_types dictionary missing key boolean"
    assert 'categorical' in keys, "col_types dictionary missing key categorical"
    assert 'datetime' in keys, "col_types dictionary missing key datetime"
    assert 'timedelta' in keys, "col_types dictionary missing key timedelta"
    assert '.' not in filename, "filename doesn't need an extension"
    assert color in col_types['numeric'] or color is None
    assert isinstance(width, int) or width is None
    assert isinstance(height, int) or height is None

    figure_list = list()

    path_list = hierarchical_path(df=df, limit=limit,col_types=col_types )

    numeric_cols = col_types['numeric']

    if len(path_list) > 1:
        for col in numeric_cols:

            plot = px.sunburst(data_frame=df,
                               color=color,
                               path=path_list,
                               values=col,width=width, height=height,
                               title='Sunburst chart of {} across paths {}'.format(col, str(path_list))
                               )

            figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_correlation_plot(df,
                            correlation_method='pearson',
                            create_html=False,
                            width=None,
                            height=None,
                            filename='correlation_plot'):
    """
    Creates a correlation plot for the provided dataframe
    based on the correlation method supplied and returns a list of plotly graph objects
    :param df: pandas dataframe
    :param correlation_method: str, method for computing correlation, one of kendall, pearson, spearman
    :param create_html: boolean, whether to create html file or not
    :param filename:str, name of file, the extension is excluded
    :return: list of graph objects
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(create_html, bool), "create_html must be a boolean"
    assert isinstance(correlation_method, str), "correlation method must be a string"
    assert isinstance(filename, str), "filename must be a string with a dot or an extension"
    assert '.' not in filename, "filename doesn't need an extension"
    assert correlation_method in ['pearson', 'kendall', 'spearman']
    assert isinstance(width, int) or width is None
    assert isinstance(height, int) or height is None

    figure_list = list()

    if len(extract_numeric_cols(df=df))>1:

        correlation = calculate_correlation(df=df, method=correlation_method)

        plot = px.imshow(img=correlation,width=width, height=height,
                         title='Correlation plot using {} method'.format(correlation_method))

        figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_histogram(df,
                     numeric_cols,
                     nbins=20,
                     marginal=None,
                     width=None,
                     height=None,
                     cumulative=False,
                     histfunc='sum',
                     histnorm=None,
                     filename='histogram',
                     create_html=True,
                     orientation='v',
                     color=None
                     ):
    """

    :param df: pandas dataframe
    :param numeric_cols:list of columns with numeric columns
    :param nbins:int, number of bins
    :param marginal:str, marginal must be one of 'rug','box','violin','histogram
    :param cumulative:bool
    :param histfunc:str, histfunc must be one of 'count', 'sum', 'avg','min','max'
    :param histnorm:str, normalization method for histogram 'percent','probability','density','probability density'
    :param filename: str, name of file, the extension must be excluded
    :param create_html: boolean, whether to create an html file or not
    :param orientation: str, the orientation of the figure, 'v' or 'h'
    :return:list which contains plotly graph objects
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(numeric_cols, list), "numeric_cols must be a list"
    assert isinstance(nbins, int), "nbins must be an integer"
    assert marginal in ['rug','box','violin','histogram',None], "marginal options 'rug','box','violin','histogram'"
    assert isinstance(cumulative, bool), "cumulative must be a boolean"
    assert histfunc in ['count', 'sum', 'avg', 'min',
                        'max'], "histfunc must be one of 'count', 'sum', 'avg','min','max' "
    assert histnorm in ['percent', 'probability', 'density', 'probability density', None]
    assert isinstance(filename, str), "filename must be a string with a dot or an extension"
    assert '.' not in filename, "filename doesn't need an extension"
    assert isinstance(create_html, bool), "create_html must be a boolean"
    assert orientation in ['v','h']
    assert isinstance(width, int) or width is None
    assert isinstance(height, int) or height is None

    figure_list = list()

    if check_numeric(df=df,column_list=numeric_cols):
        for col in numeric_cols:
            plot = px.histogram(data_frame=df,
                                nbins=nbins,
                                x=col,
                                width=width,
                                height=height,
                                marginal=marginal,
                                cumulative=cumulative,
                                histfunc=histfunc,
                                histnorm=histnorm,
                                orientation=orientation,
                                title='Distribution of {}'.format(col),
                                color=color
                                )
            figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_scatter(df,
                   col_types,
                   filename='scatter',
                   marginal_x=None,
                   width=None,
                   height=None,
                   marginal_y=None,
                   log_x=False,
                   log_y=False,
                   orientation='v',size=None,
                   opacity=1.0,
                   maximum_color_groups=5,
                   create_html=True):
    """
    :param df:
    :param col_types: dictionary that contains mapping of column type to list of column names
                    It is the output of extract_col_types in tabular module
    :param filename:str, name of file, the extension must be excluded
    :param marginal_x:options for including marginal charts on x axis
    :param marginal_y:options for including marginal charts on y axis
    :param log_x:boolean, whether to create a log axis
    :param log_y:boolean, whether to create a log axis
    :param orientation: str, the orientation of the figure, 'v' or 'h'
    :param create_html: boolean, whether to create an html file or not
    :param opacity: float, value between 0 and 1. Sets the opacity for markers
    :param maximum_color_groups: int, maximum number of color groups in the scatter plot
    :return:list which contains plotly graph objects
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(col_types, dict), "col_types must be a dictionary with column " \
                                        "name as keys and column type as value"
    keys = col_types.keys()
    assert 'numeric' in keys, "col_types dictionary missing key numeric"
    assert 'object' in keys, "col_types dictionary missing key object"
    assert 'boolean' in keys, "col_types dictionary missing key boolean"
    assert 'categorical' in keys, "col_types dictionary missing key categorical"
    assert 'datetime' in keys, "col_types dictionary missing key datetime"
    assert 'timedelta' in keys, "col_types dictionary missing key timedelta"
    assert isinstance(filename, str), "filename must be a string with a dot or an extension"
    assert '.' not in filename, "filename doesn't need an extension"
    assert isinstance(log_y, bool)
    assert isinstance(log_x, bool)
    assert marginal_x in ['rug', 'box', 'violin', 'histogram',None], "marginal must be one of 'rug'," \
                                                                     "'box','violin','histogram'"
    assert marginal_y in ['rug', 'box', 'violin', 'histogram',None], "marginal must be one of 'rug'," \
                                                                     "'box','violin','histogram'"
    assert isinstance(opacity, float), "opacity must be a float"
    assert opacity <= 1.0, "opacity must be between 0 and 1"
    assert opacity >= 0.0,"opacity must be a float between 0 and 1"
    assert isinstance(create_html, bool), "create_html must be a boolean"
    assert orientation in ['v', 'h']
    assert isinstance(maximum_color_groups, int)
    assert isinstance(width, int) or width is None
    assert isinstance(height, int) or height is None


    figure_list = list()
    numeric_cols = col_types['numeric']

    if len(numeric_cols) < 2:
        # scatter plots need at least 2 columns of numeric type
        return figure_list
    plot_pairs = create_pairs(df, numeric_cols=numeric_cols)

    columns_with_distinct = columns_with_distinct_values(df,
                                                         maximum_number_distinct_values=maximum_color_groups,
                                                         categorical_only=True)
    if len(columns_with_distinct) == 0:
        columns_with_distinct.append(None)

    for pair in plot_pairs:
        x,y = pair
        for color in columns_with_distinct:
            plot = px.scatter(data_frame=df,
                              x=x,
                              y=y,width=width, height=height,
                              log_y=log_y,
                              log_x=log_x,
                              opacity=opacity,
                              orientation=orientation,
                              marginal_x=marginal_x,
                              marginal_y=marginal_y,
                              size=size,
                              color=color,
                              title='Plot of {} vs {} with color {}'.format(x,y,color))
            figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list


def create_density_chart(df,
                         col_types,
                         nbinsx=None,
                         nbinsy=None,
                         width=None,
                         height=None,
                         maximum_color_groups=4,
                         typr_of_chart='contour',
                         filename='density_charts',
                         orientation='v',
                         marginal_x=None,
                         marginal_y=None,
                         log_x=False,
                         log_y=False,
                         histfunc='sum',
                         histnorm=None,
                         create_html=True
                         ):
    """
    Create density chart and density heatmap charts
    :param df: pandas dataframe
    :param col_types:  dictionary that contains mapping of column type to list of column names
                    It is the output of extract_col_types in tabular module
    :param nbinsx: int, number of bins on x axis
    :param nbinsy: int, number of bins on y axis
    :param maximum_color_groups: int, maximum number of color groups in the density charts
    :param typr_of_chart: str, 'contour' or 'heatmap'
    :param filename: str, name of file, the extension must be excluded
    :param orientation: str, the orientation of the figure, 'v' or 'h'
    :param marginal_x: options for including marginal charts on x axis, one of 'rug', 'box', 'violin', 'histogram',None
    :param marginal_y: options for including marginal charts on y axis, one of 'rug', 'box', 'violin', 'histogram',None
    :param log_x: boolean, whether to create a log x axis
    :param log_y: boolean, whether to create a log y axis
    :param histfunc: histfunc must be one of 'count', 'sum', 'avg','min','max'
    :param histnorm: str, normalization method for histogram 'percent','probability','density','probability density'
    :param create_html: boolean, whether to create an html file or not
    :return:list which contains plotly graph objects
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
    assert isinstance(col_types, dict), "col_types must be a dictionary with column " \
                                        "name as keys and column type as value"
    keys = col_types.keys()
    assert 'numeric' in keys, "col_types dictionary missing key numeric"
    assert 'object' in keys, "col_types dictionary missing key object"
    assert 'boolean' in keys, "col_types dictionary missing key boolean"
    assert 'categorical' in keys, "col_types dictionary missing key categorical"
    assert 'datetime' in keys, "col_types dictionary missing key datetime"
    assert 'timedelta' in keys, "col_types dictionary missing key timedelta"
    assert isinstance(nbinsx,int) or nbinsx is None
    assert isinstance(nbinsy, int) or nbinsy is None
    assert isinstance(log_y, bool)
    assert isinstance(log_x, bool)
    assert marginal_x in ['rug', 'box', 'violin', 'histogram',None], "marginal must be one of 'rug'," \
                                                                     "'box','violin','histogram'"
    assert marginal_y in ['rug', 'box', 'violin', 'histogram',None], "marginal must be one of 'rug'," \
                                                                     "'box','violin','histogram'"
    assert histfunc in ['count', 'sum', 'avg', 'min',
                        'max'], "histfunc must be one of 'count', 'sum', 'avg','min','max' "
    assert histnorm in ['percent', 'probability', 'density', 'probability density', None]
    assert orientation in ['v', 'h']
    assert isinstance(filename, str), "filename must be a string with a dot or an extension"
    assert '.' not in filename, "filename doesn't need an extension"
    assert typr_of_chart in ['contour','heatmap']
    assert isinstance(width, int) or width is None
    assert isinstance(height, int) or height is None
    # assert width > 0 or width is None
    # assert height > 0 or height is None

    figure_list = list()
    numeric_cols = col_types['numeric']

    if len(numeric_cols) < 2:
        # density contour at least 2 columns of numeric type
        return figure_list

    # create pairing for x and y values
    plot_pairs = create_pairs(df, numeric_cols=numeric_cols)

    columns_with_distinct = columns_with_distinct_values(df,
                                                         maximum_number_distinct_values=maximum_color_groups,
                                                         categorical_only=True)

    if len(columns_with_distinct) == 0:
        columns_with_distinct.append(None)

    for pair in plot_pairs:
        x,y = pair
        for z in numeric_cols:
            if typr_of_chart == 'contour':
                for color in columns_with_distinct:
                    title = "Density contour of {} vs {},with {} on z axis".format(x, y, z)
                    plot = px.density_contour(data_frame=df,
                                              x=x,
                                              y=y,
                                              z=z,width=width, height=height,
                                              color=color,
                                              histnorm=histnorm,
                                              histfunc=histfunc,
                                              nbinsx=nbinsx,
                                              nbinsy=nbinsy,
                                              log_y=log_y,
                                              log_x=log_x,
                                              marginal_x=marginal_x,
                                              marginal_y=marginal_y,
                                              orientation=orientation,
                                              title=title)
                    figure_list.append(plot)

            if typr_of_chart == 'heatmap':
                title = "Density heatmap of {} vs {},with {} on z axis".format(x, y, z)

                plot = px.density_heatmap(data_frame=df,
                                          x=x,
                                          y=y,
                                          z=z,
                                          width=width,
                                          height=height,
                                          histnorm=histnorm,
                                          histfunc=histfunc,
                                          nbinsx=nbinsx,
                                          nbinsy=nbinsy,
                                          log_y=log_y,
                                          log_x=log_x,
                                          marginal_x=marginal_x,
                                          marginal_y=marginal_y,
                                          orientation=orientation,
                                          title=title)
                figure_list.append(plot)

    if create_html:
        figures_to_html(figs=figure_list, filename=filename)

    return figure_list

















