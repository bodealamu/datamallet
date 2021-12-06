from datamallet.visualization.utils import (pie_sectors,
                                            treemap_path,create_pairs,
                                            column_use,
                                            figures_to_html)
from datamallet.tabular.utils import (extract_col_types,
                                      check_dataframe,
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
                  numeric_cols,
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
    :param numeric_cols: list of column names with numeric data type
    :param filename: str, filename for the html file
    :param create_html: boolean, whether to create an html file or not
    :param violinmode: str, how you want the charts to be displayed
    :param points: str, how the points in the violin chart should be displayed
    :param display_box: boolean, whether to display a box within the violin chart
    :param color:
    :return:
    """
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
    :param create_html:boolean, whether to create an html file or not
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


def create_sunburst(df, numeric_cols,
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


def create_scatter(df, basic=True,
                   filename='scatter',
                   marginal_x=None,
                   marginal_y=None,
                   log_x=False,
                   log_y=False,
                   create_html=True):
    """

    :param df:
    :param basic:boolean, whether to create a basic scatterplot or not
    :param filename:
    :param marginal_x:options for including marginal charts on x axis
    :param marginal_y:options for including marginal charts on y axis
    :param log_x:boolean, whether to create a log axis
    :param log_y:boolean, whether to create a log axis
    :param create_html: boolean, whether to create an html file or not
    :return:
    """
    plot_pairs = create_pairs(df)

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


class AutoPlot(object):
    def __init__(self,
                 df,
                 nbins=None,
                 marginals=None,
                 cumulative=False,
                 filename='autoplot',
                 box_points='outliers',
                 boxmode='group',
                 box_notched=False,
                 log_x=False,
                 log_y=False,
                 size=None,
                 histfunc=None,
                 histnorm=None,
                 include_box=True,
                 include_treemap=True,
                 include_sunburst=True,
                 include_correlation=False,
                 include_pie=True,
                 include_histogram=True,
                 include_violin=True,
                 violinmode='group',
                 violin_box=True,
                 violin_points='all',
                 treemap_path_limit=2,
                 sunburst_path_limit=2,
                 correlation_method='pearson',
                 maximum_number_sectors=3,
                 pie_chart_hole=False,
                 create_html=True
                 ):
        """
        Entry point for automated data visualization
        :param df:
        :param nbins:
        :param marginals:
        :param cumulative:
        :param filename:
        :param box_points:
        :param boxmode:
        :param box_notched:
        :param log_x:
        :param log_y:
        :param size:
        :param histfunc:
        :param histnorm:
        :param include_box: boolean, whether to include box plots
        :param include_treemap: boolean, whether to include treemaps
        :param include_sunburst: boolean, whether to include sunburst
        :param include_correlation: boolean, whether to include correlation plot
        :param include_pie: boolean, whether to include pie
        :param include_histogram: boolean, whether to include histogram
        :param include_violin: boolean, whether to include violin plots
        :param violinmode: str, display mode for violin charts
        :param violin_box: boolean, whether to include box plot in violin
        :param violin_points: str, how to display points in a violin plot
        :param treemap_path_limit:
        :param sunburst_path_limit:
        :param correlation_method: str, method to use to compute correlation
        :param maximum_number_sectors: int, maximum number of sectors in pie charts
        :param pie_chart_hole: boolean, whether to include a hole in pie chart or not
        :param create_html:
        """
        self.df = df
        self.nbins = nbins
        self.marginals = marginals
        self.cumulative = cumulative
        self.filename = filename
        self.points = box_points
        self.boxmode = boxmode
        self.notched = box_notched
        self.log_x = log_x
        self.log_y = log_y
        self.size = size
        self.histfunc = histfunc
        self.histnorm = histnorm
        self.column_types = extract_col_types(df=df)
        self.include_box = include_box
        self.include_treemap = include_treemap
        self.include_sunburst = include_sunburst
        self.include_correlation = include_correlation
        self.include_pie = include_pie
        self.include_histogram = include_histogram
        self.include_violin = include_violin
        self.violinmode = violinmode
        self.violin_box = violin_box
        self.violin_points = violin_points
        self.treemap_path_limit = treemap_path_limit
        self.sunburst_path_limit = sunburst_path_limit
        self.correlation_method = correlation_method
        self.maximum_number_sectors = maximum_number_sectors
        self.create_html = create_html
        self.pie_chart_hole = pie_chart_hole
        self.pie_sectors = pie_sectors(df=self.df, maximum_number_sectors=self.maximum_number_sectors)

    def chart_type(self):
        column_types = self.column_types
        numeric_cols = column_types['numeric']
        datetime_cols = column_types['datetime']
        timedelta_cols = column_types['timedelta']
        categorical_cols = column_types['categorical']
        boolean_cols = column_types['boolean']
        object_cols = column_types['object']

        chart_types = list()

        if len(numeric_cols) > 1:
            chart_types.append('scatter')
            chart_types.append('correlation_plot')
        if len(numeric_cols) > 0:
            chart_types.append('histogram')
            chart_types.append('boxplot')
            chart_types.append('violinplot')
        if len(categorical_cols) >0 or len(boolean_cols) > 0 or len(object_cols):
            chart_types.append('treemaps')
            chart_types.append('sunburst')
        if len(datetime_cols) !=0 or len(timedelta_cols) != 0:
            chart_types.append('timeseries_plot')
        if len(self.pie_sectors) !=0:
            chart_types.append('pie')

        return chart_types

    def plot(self):
        chart_types = self.chart_type()

        object_cols = self.column_types['object']
        boolean_cols = self.column_types['boolean']
        categorical_cols = self.column_types['categorical']
        numeric_cols = self.column_types['numeric']

        categorical = list()
        categorical.extend(object_cols)
        categorical.extend(boolean_cols)
        categorical.extend(categorical_cols)

        figure_list = list()

        if len(chart_types) != 0:
            for chart in chart_types:
                if chart == 'pie' and self.include_pie:

                    pie_list = create_pie(df=self.df,
                                            numeric_cols=numeric_cols,
                                            pie_sector=self.pie_sectors,
                                            create_html=False,
                                            hole=self.pie_chart_hole,
                                            filename='pie')

                    figure_list.extend(pie_list)
                if chart == 'scatter':
                    if len(categorical) == 0:
                        scatter_plot_list = create_scatter(df=self.df,
                                                             basic=True,
                                                             marginal_x=self.marginals,
                                                             marginal_y=self.marginals,
                                                             log_x=self.log_x,
                                                             log_y=self.log_y,
                                                             create_html=False)

                    else:
                        scatter_plot_list = create_scatter(df=self.df,
                                                             basic=False,
                                                             marginal_x=self.marginals,
                                                             marginal_y=self.marginals,
                                                             log_x=self.log_x,
                                                             log_y=self.log_y,
                                                             create_html=False)

                    figure_list.extend(scatter_plot_list)

                if chart == 'correlation_plot' and self.include_correlation:
                    correlation_plot_list = create_correlation_plot(df=self.df,
                                                                      correlation_method=self.correlation_method)
                    figure_list.extend(correlation_plot_list)

                if chart == 'histogram' and self.include_histogram:
                    histogram_list = create_histogram(df=self.df,
                                                        numeric_cols=numeric_cols,
                                                        nbins=self.nbins,
                                                        marginal=self.marginals,
                                                        cumulative=self.cumulative,
                                                        histfunc=self.histfunc,
                                                        histnorm=self.histnorm,
                                                        filename='histogram',
                                                        create_html=False)

                    figure_list.extend(histogram_list)

                if chart == 'boxplot' and self.include_box:
                    box_list = create_box(df=self.df,
                                            numeric_cols=numeric_cols,
                                            points=self.points,
                                            boxmode=self.boxmode,
                                            notched=self.notched,
                                            color=None,
                                            filename='box',
                                            create_html=False)

                    figure_list.extend(box_list)

                if chart == 'treemaps' and self.include_treemap:
                    treemap_list = create_treemap(df=self.df,
                                                    numeric_cols=numeric_cols,
                                                    create_html=False,
                                                    filename='treemap',
                                                    limit=self.treemap_path_limit
                                                    )
                    figure_list.extend(treemap_list)

                if chart == 'sunburst' and self.include_sunburst:
                    sunburst_list = create_sunburst(df=self.df,
                                                      numeric_cols=numeric_cols,
                                                      create_html=False,
                                                      filename='sunburst',
                                                      limit=self.sunburst_path_limit
                                                      )
                    figure_list.extend(sunburst_list)

                if chart == 'violinplot' and self.include_violin:
                    violin_list = create_violin(df=self.df,
                                                  numeric_cols=numeric_cols,
                                                  filename='violin',
                                                  create_html=False,
                                                  points=self.violin_points,
                                                  display_box=self.violin_box,
                                                  color=None)

                    figure_list.extend(violin_list)

        if self.create_html:
            figures_to_html(figs=figure_list, filename=self.filename)

        return figure_list










