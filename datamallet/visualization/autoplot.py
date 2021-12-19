from .plot import (create_pie,
                   create_box,
                   create_scatter,
                   create_treemap,
                   create_violin,
                   create_sunburst,
                   create_correlation_plot,
                   create_histogram)
from .utils import (columns_with_distinct_values,
                    extract_col_types,
                    figures_to_html)


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
                 include_scatter=False,
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
                 maximum_number_boxplots=5,
                 maximum_number_violinplots=5,
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
        :param include_scatter: boolean, whether to include scatter plots
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
        :param maximum_number_boxplots:int, maximum_number_boxplots
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
        self.include_scatter = include_scatter
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
        self.maximum_number_boxplots = maximum_number_boxplots
        self.maximum_number_violinplots = maximum_number_violinplots
        self.create_html = create_html
        self.pie_chart_hole = pie_chart_hole
        self.pie_sectors = columns_with_distinct_values(df=self.df, categorical_only=True,
                                                        maximum_number_distinct_values=self.maximum_number_sectors)

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

    def show(self):
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
                                          create_html=False,
                                          hole=self.pie_chart_hole,
                                          filename='pie')

                    figure_list.extend(pie_list)
                if chart == 'scatter' and self.include_scatter:
                    if len(categorical) == 0:
                        scatter_plot_list = create_scatter(df=self.df,
                                                           col_types= self.column_types,
                                                             basic=True,
                                                             marginal_x=self.marginals,
                                                             marginal_y=self.marginals,
                                                             log_x=self.log_x,
                                                             log_y=self.log_y,
                                                             create_html=False)

                    else:
                        scatter_plot_list = create_scatter(df=self.df,
                                                           col_types= self.column_types,
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
                                          maximum_number_boxplots=self.maximum_number_boxplots,
                                          col_types= self.column_types,
                                          points=self.points,
                                          boxmode=self.boxmode,
                                          notched=self.notched,
                                          color=None,
                                          filename='box',
                                          create_html=False)

                    figure_list.extend(box_list)

                if chart == 'treemaps' and self.include_treemap:
                    treemap_list = create_treemap(df=self.df,
                                                    col_types=self.column_types,
                                                    create_html=False,
                                                    filename='treemap',
                                                    limit=self.treemap_path_limit
                                                    )
                    figure_list.extend(treemap_list)

                if chart == 'sunburst' and self.include_sunburst:
                    sunburst_list = create_sunburst(df=self.df,
                                                      col_types=self.column_types,
                                                      create_html=False,
                                                      filename='sunburst',
                                                      limit=self.sunburst_path_limit
                                                      )
                    figure_list.extend(sunburst_list)

                if chart == 'violinplot' and self.include_violin:
                    violin_list = create_violin(df=self.df,
                                                col_types= self.column_types,
                                                maximum_number_violinplots=self.maximum_number_violinplots,
                                                filename='violin',
                                                create_html=False,
                                                points=self.violin_points,
                                                display_box=self.violin_box,
                                                color=None)

                    figure_list.extend(violin_list)

        if self.create_html:
            figures_to_html(figs=figure_list, filename=self.filename)

        return figure_list
