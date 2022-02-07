from .plot import (create_pie,
                   create_box,
                   create_scatter,
                   create_treemap,
                   create_violin,
                   create_sunburst,
                   create_correlation_plot,create_density_chart,
                   create_histogram)
from .utils import (columns_with_distinct_values,
                    extract_col_types,
                    figures_to_html)
import pandas as pd


class AutoPlot(object):
    def __init__(self,
                 df,
                 nbins=30,
                 nbinsy=30,
                 scatter_maximum_color_groups=5,
                 marginal_x=None,
                 marginal_y=None,
                 cumulative=False,
                 filename='autoplot',
                 box_points='outliers',
                 boxmode='group',
                 box_notched=False,
                 log_x=False,
                 log_y=False,
                 size=None,
                 histfunc='count',
                 histnorm=None,
                 include_scatter=False,
                 include_box=True,
                 include_treemap=True,
                 include_sunburst=True,
                 include_correlation=False,
                 include_pie=True,
                 include_histogram=True,
                 include_violin=True,
                 include_density_heatmap=True,
                 include_density_contour=True,
                 violinmode='group',
                 violin_box=True,
                 violin_points='all',
                 treemap_path_limit=2,
                 sunburst_path_limit=2,
                 correlation_method='pearson',
                 maximum_number_sectors=3,
                 maximum_number_boxplots=5,
                 maximum_number_violinplots=5,
                 density_max_color_groups=2,
                 pie_chart_hole=False,
                 create_html=True,
                 orientation='v',
                 opacity=1.0,
                 color=None,
                 color_hierachical_charts=None,
                 width=None,
                 height=None
                 ):
        """
        Entry point for automated data visualization
        :param df: pandas dataframe
        :param nbins:int, number of bins on x axis
        :param nbinsy:int, number of bins on y axis
        :param marginals:str, marginal must be one of 'rug','box','violin','histogram
        :param cumulative:
        :param filename:str, filename for the html file
        :param box_points:str, whether to show the points in a box plot possible options are 'outliers', 'all',False,
                 'suspectedoutliers'
        :param boxmode:str, how to display the boxes in a boxplot.
                    Options are 'group' or 'overlay'. In group mode,
                    boxes are placed beside each other, in overlay mode,
                    boxes are placed on top of each other.
        :param box_notched:boolean, True or False, boxes are drawn with notches
        :param log_x:boolean, whether to create a log x axis
        :param log_y:boolean, whether to create a log y axis
        :param size:column name to use for size parameter
        :param histfunc: str, histfunc must be one of 'count', 'sum', 'avg','min','max'
        :param histnorm:str, normalization method for histogram 'percent','probability','density','probability density'
        :param include_scatter: boolean, whether to include scatter plots
        :param include_box: boolean, whether to include box plots
        :param include_treemap: boolean, whether to include treemaps
        :param include_sunburst: boolean, whether to include sunburst
        :param include_correlation: boolean, whether to include correlation plot
        :param include_pie: boolean, whether to include pie
        :param include_histogram: boolean, whether to include histogram
        :param include_violin: boolean, whether to include violin plots
        :param include_density_heatmap:boolean, whether to include density heatmap charts
        :param include_density_contour: boolean, whether to include density contour charts
        :param violinmode: str, display mode for violin charts
        :param violin_box: boolean, whether to include box plot in violin
        :param violin_points: str, how to display points in a violin plot
        :param treemap_path_limit:int, represents the depth of treemap
        :param sunburst_path_limit:int, represents the depth of sunburst chart
        :param correlation_method: str, method to use to compute correlation
        :param maximum_number_sectors: int, maximum number of sectors in pie charts
        :param maximum_number_boxplots:int, maximum_number_boxplots
        :param density_max_color_groups:int, maximum number of color points in density chart
        :param pie_chart_hole: boolean, whether to include a hole in pie chart or not
        :param create_html:boolean, whether to create an html file or not
        :param orientation: str, orientation of the figure, 'v' or 'h'
        :param opacity:float, opacity set for the markers, value between 0 and 1
        :param color: str, color option for boxplots
        :param color_hierachical_charts: str, color option for treemaps and sunburst charts

        Usage
        >>> import pandas as pd
        >>> from datamallet.visualization import AutoPlot
        >>> df3 = pd.DataFrame({'A':[1,1,2,1,1], 'B':[2,2,1,2,0],})
        >>> autoplot1 = AutoPlot(df=df3,filename='autoplot' ,create_html=True,include_scatter=True)
        >>> print(autoplot1.chart_type()) # output may change as more chart types are added

        ['scatter', 'correlation_plot', 'histogram', 'boxplot', 'violinplot']

        >>> autoplot1.show()
        # creates a file autoplot.html based on the filename you provide, all charts would be found there

        """
        self.df = df
        self.nbins = nbins
        self.nbinsy = nbinsy
        self.scatter_maximum_color_groups = scatter_maximum_color_groups
        self.orientation = orientation
        self.opacity=opacity
        self.color = color
        self.marginal_x = marginal_x
        self.marginal_y = marginal_y
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
        self.include_scatter = include_scatter
        self.include_box = include_box
        self.include_treemap = include_treemap
        self.include_sunburst = include_sunburst
        self.include_correlation = include_correlation
        self.include_pie = include_pie
        self.include_histogram = include_histogram
        self.include_violin = include_violin
        self.include_density_contour = include_density_contour
        self.include_density_heatmap = include_density_heatmap
        self.violinmode = violinmode
        self.violin_box = violin_box
        self.violin_points = violin_points
        self.treemap_path_limit = treemap_path_limit
        self.sunburst_path_limit = sunburst_path_limit
        self.correlation_method = correlation_method
        self.maximum_number_sectors = maximum_number_sectors
        self.maximum_number_boxplots = maximum_number_boxplots
        self.maximum_number_violinplots = maximum_number_violinplots
        self.density_max_color_groups = density_max_color_groups
        self.create_html = create_html
        self.pie_chart_hole = pie_chart_hole
        self.color_hierachical_charts = color_hierachical_charts
        self.pie_sectors = columns_with_distinct_values(df=self.df, categorical_only=True,
                                                        maximum_number_distinct_values=self.maximum_number_sectors)
        self.width = width
        self.height = height
        assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"
        assert isinstance(nbins, int) or nbins is None, "nbins must be an integer or None"
        assert isinstance(nbinsy, int) or nbinsy is None, "nbinsy must be an integer or None"
        assert isinstance(scatter_maximum_color_groups, int),'scatter_maximum_color_groups must be an int'
        assert marginal_x in ['rug', 'box', 'violin', 'histogram', None]
        assert marginal_y in ['rug', 'box', 'violin', 'histogram', None]
        assert isinstance(cumulative, bool), "cumulative must be a boolean"
        assert '.' not in filename, "filename doesn't need an extension"
        assert isinstance(filename, str), "filename must be a string with a dot or an extension"
        assert box_points in ['all', 'outliers', 'suspectedoutliers', False], "accepted values for points 'all', " \
                                                                          "'outliers', " \
                                                                          "'suspectedoutliers'"
        assert boxmode in ['group', 'overlay'], "boxmode must be either group or overlay"
        assert isinstance(box_notched, bool), "notched must be a boolean"
        assert isinstance(log_y, bool),"log_x must be a boolean"
        assert isinstance(log_x, bool),"log_y must be a boolean"
        assert size in self.column_types['numeric'] or size is None, "size must be the name of a numeric column or None"
        assert histnorm in ['percent', 'probability', 'density', 'probability density', None]
        assert histfunc in ['count', 'sum', 'avg', 'min',
                            'max'], "histfunc must be one of 'count', 'sum', 'avg','min','max' "
        assert isinstance(include_pie, bool)
        assert isinstance(include_treemap,bool)
        assert isinstance(include_box, bool)
        assert isinstance(include_correlation, bool)
        assert isinstance(include_histogram, bool)
        assert isinstance(include_scatter,bool)
        assert isinstance(include_sunburst,bool)
        assert isinstance(include_violin, bool)
        assert isinstance(include_density_contour,bool)
        assert isinstance(include_density_heatmap,bool)
        assert violinmode in ['group', 'overlay'], "violinmode must be either group or overlay"
        assert isinstance(violin_box, bool)
        assert violin_points in ['all', 'outliers', 'suspectedoutliers', False]
        assert treemap_path_limit > 1
        assert sunburst_path_limit > 1
        assert correlation_method in ['pearson', 'kendall', 'spearman']
        assert maximum_number_sectors > 1,"maximumnumber_sectors must be an int greater than 1"
        assert isinstance(maximum_number_sectors,int), "maximum_number_sectors must be an int"
        assert isinstance(maximum_number_boxplots,int), "maximum_number_boxplots must be an int"
        assert isinstance(maximum_number_violinplots,int), "maximum_number_violinplots must be an int"
        assert isinstance(density_max_color_groups, int), "density_max_color_groups must be an int"
        assert isinstance(pie_chart_hole, bool),"pie_chart_hole must be a boolean"
        assert isinstance(create_html, bool),"create_html must be a boolean"
        assert orientation in ['v', 'h'],"orientation must be a string with either v or h"
        assert isinstance(opacity, float), "opacity must be a float"
        assert opacity <= 1.0, "opacity must be a float"
        assert opacity >= 0.0, "opacity must be a number between 0 and 1"
        assert isinstance(color,str) or color is None, "color must be a string"
        col_types = self.column_types
        cat_cols = col_types['categorical']
        bool_cols = col_types['boolean']
        obj_cols = col_types['object']
        assert (color in cat_cols) or (color in bool_cols) or (color in obj_cols) or color is None
        assert color_hierachical_charts in self.column_types['numeric'] or color_hierachical_charts is None, "color_hierachical_charts must be the name of a numeric column or None"
        assert isinstance(width, int) or width is None
        assert isinstance(height, int) or height is None

    def chart_type(self):
        """
        Function for determining the eligible chart types
        :return: list of charts which should be made based on the supplied dataframe

         Usage
        >>> import pandas as pd
        >>> from datamallet.visualization import AutoPlot
        >>> df3 = pd.DataFrame({'A':[1,1,2,1,1], 'B':[2,2,1,2,0],})
        >>> autoplot1 = AutoPlot(df=df3,filename='autoplot' ,create_html=True,include_scatter=True)
        >>> print(autoplot1.chart_type()) # output may change as more chart types are added

        ['scatter', 'correlation_plot', 'histogram', 'boxplot', 'violinplot']
        """
        column_types = self.column_types
        numeric_cols = column_types['numeric']
        datetime_cols = column_types['datetime']
        timedelta_cols = column_types['timedelta']
        categorical_cols = column_types['categorical']
        boolean_cols = column_types['boolean']
        object_cols = column_types['object']

        chart_types = list()

        if len(numeric_cols) == 0:
            # if no numeric columns,no charts can be made, return empty list
            return chart_types

        if len(numeric_cols) > 1:
            chart_types.append('scatter')
            chart_types.append('correlation_plot')
            chart_types.append('density_contour')
            chart_types.append('density_heatmap')
        if len(numeric_cols) > 0:
            chart_types.append('histogram')
            chart_types.append('boxplot')
            chart_types.append('violinplot')
        if len(categorical_cols) >0 or len(boolean_cols) > 0 or len(object_cols) > 0:
            chart_types.append('treemaps')
            chart_types.append('sunburst')
        if len(datetime_cols) !=0 or len(timedelta_cols) != 0:
            chart_types.append('timeseries_plot')
        if len(self.pie_sectors) !=0:
            chart_types.append('pie')

        return chart_types

    def show(self):
        """
        Plotting function, creates the charts in an html file
        :return: list of plotly graph objects
        """
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
                                          list_of_categorical_columns=self.pie_sectors,
                                          opacity=self.opacity,width=self.width,height=self.height,
                                          create_html=False,
                                          hole=self.pie_chart_hole,
                                          filename='pie')

                    figure_list.extend(pie_list)
                if chart == 'scatter' and self.include_scatter:

                    scatter_plot_list = create_scatter(df=self.df,
                                                       size=self.size,
                                                       col_types= self.column_types,
                                                       marginal_y=self.marginal_x,
                                                       marginal_x=self.marginal_y,
                                                       orientation=self.orientation,
                                                       opacity=self.opacity,width=self.width,height=self.height,
                                                       maximum_color_groups=self.scatter_maximum_color_groups,
                                                       log_x=self.log_x,
                                                       log_y=self.log_y,
                                                       create_html=False)

                    figure_list.extend(scatter_plot_list)

                if chart == 'correlation_plot' and self.include_correlation:
                    correlation_plot_list = create_correlation_plot(df=self.df,
                                                                    create_html=False,
                                                                    width=self.width,
                                                                    height=self.height,
                                                                    correlation_method=self.correlation_method)
                    figure_list.extend(correlation_plot_list)

                if chart == 'histogram' and self.include_histogram:
                    histogram_list = create_histogram(df=self.df,
                                                      numeric_cols=numeric_cols,
                                                      nbins=self.nbins,
                                                      width=self.width,
                                                      height=self.height,
                                                      marginal=self.marginal_x,
                                                      cumulative=self.cumulative,
                                                      histfunc=self.histfunc,
                                                      histnorm=self.histnorm,
                                                      filename='histogram',
                                                      create_html=False,
                                                      orientation=self.orientation)

                    figure_list.extend(histogram_list)

                if chart == 'boxplot' and self.include_box:
                    box_list = create_box(df=self.df,
                                          maximum_number_boxplots=self.maximum_number_boxplots,
                                          col_types= self.column_types,
                                          points=self.points,
                                          width=self.width,
                                          height=self.height,
                                          boxmode=self.boxmode,
                                          notched=self.notched,
                                          color=self.color,
                                          filename='box',
                                          create_html=False)

                    figure_list.extend(box_list)

                if chart == 'treemaps' and self.include_treemap:
                    treemap_list = create_treemap(df=self.df,
                                                  col_types=self.column_types,
                                                  create_html=False,
                                                  width=self.width,
                                                  height=self.height,
                                                  color=self.color_hierachical_charts,
                                                  filename='treemap',
                                                  limit=self.treemap_path_limit)
                    figure_list.extend(treemap_list)

                if chart == 'sunburst' and self.include_sunburst:
                    sunburst_list = create_sunburst(df=self.df,
                                                    col_types=self.column_types,
                                                    create_html=False,
                                                    width=self.width,
                                                    height=self.height,
                                                    color=self.color_hierachical_charts,
                                                    filename='sunburst',
                                                    limit=self.sunburst_path_limit)

                    figure_list.extend(sunburst_list)

                if chart == 'violinplot' and self.include_violin:
                    violin_list = create_violin(df=self.df,
                                                col_types= self.column_types,
                                                maximum_number_violinplots=self.maximum_number_violinplots,
                                                filename='violin',
                                                width=self.width,
                                                height=self.height,
                                                create_html=False,
                                                points=self.violin_points,
                                                display_box=self.violin_box,
                                                color=self.color)

                    figure_list.extend(violin_list)

                if chart == 'density_contour' and self.include_density_contour:
                    density_contour_list = create_density_chart(df=self.df,
                                                                col_types=self.column_types,
                                                                nbinsx=self.nbins,
                                                                nbinsy=self.nbinsy,
                                                                width=self.width,
                                                                height=self.height,
                                                                maximum_color_groups=self.density_max_color_groups,
                                                                typr_of_chart='contour',
                                                                orientation=self.orientation,
                                                                marginal_x=self.marginal_x,
                                                                marginal_y=self.marginal_y,
                                                                log_x=self.log_x,
                                                                log_y=self.log_y,
                                                                histfunc=self.histfunc,
                                                                histnorm=self.histnorm,
                                                                create_html=False
                                                                )
                    figure_list.extend(density_contour_list)

                if chart == 'density_heatmap' and self.include_density_contour:
                    density_heatmap_list = create_density_chart(df=self.df,
                                                                col_types=self.column_types,
                                                                nbinsx=self.nbins,
                                                                nbinsy=self.nbinsy,
                                                                width=self.width,
                                                                height=self.height,
                                                                maximum_color_groups=self.density_max_color_groups,
                                                                typr_of_chart='heatmap',
                                                                orientation=self.orientation,
                                                                marginal_x=self.marginal_x,
                                                                marginal_y=self.marginal_y,
                                                                log_x=self.log_x,
                                                                log_y=self.log_y,
                                                                histfunc=self.histfunc,
                                                                histnorm=self.histnorm,
                                                                create_html=False
                                                                )
                    figure_list.extend(density_heatmap_list)

        if self.create_html:
            figures_to_html(figs=figure_list, filename=self.filename)

        return figure_list
