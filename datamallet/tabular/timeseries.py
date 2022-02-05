from .utils import check_dataframe, time_index
from sklearn.base import BaseEstimator, TransformerMixin


class Resampler(BaseEstimator,TransformerMixin):
    def __init__(self, rule, aggregation_method='mean'):
        """
        Resampler is a transformer for changing the frequency of the data.
        :param rule: str, or date offset representing the target resolution
                    1D represents a day
                    1H represents an hour
                    1T represents a minute
                    1S represents a second
                    1L represents a millisecond
                    1U represents a microsecond
                    1N represents a nanosecond

                    different numbers can be placed as prefix eg 2H is 2 hours frequency etc

                    more info here https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

        :param aggregation_method:str, aggregation method, one of mean, std, max, min, sum

        Usage
        >>> import pandas as pd
        >>> from datamallet.tabular.timeseries import Resampler
        >>> price = [10, 11, 9, 13, 14, 18, 17, 19,10, 11, 9, 13, 14, 18, 17, 19,50, 60, 40, 100, 50, 100, 40,10, 11, 9, 13, 14, 18, 17, 19,10,]
        >>> volume = [50, 60, 40, 100, 50, 100, 40, 50,10, 11, 9, 13, 14, 18, 17, 19,50, 60, 40, 100, 50, 100, 40,10, 11, 9, 13, 14, 18, 17, 19,10,]
        >>> d = {'price':price,'volume':volume}
        >>> df = pd.DataFrame(d)
        >>> df['week_starting'] = pd.date_range('01/01/2018',periods=32, freq='1H')
        >>> df.index = df['week_starting']
        >>> df.drop('week_starting', inplace=True, axis=1)

        >>> resampler = Resampler(rule='24H', aggregation_method='mean')
        >>> df_r = resampler.transform(X=df)
        >>> print(df_r)
                        price     volume
        week_starting
        2018-01-01     28.000  43.791667
        2018-01-02     13.875  13.875000

        """
        self.rule = rule
        self.aggregation_method = aggregation_method
        assert isinstance(rule, str), "rule must be a string"
        assert aggregation_method in ['mean','std','min','max','sum']

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.copy()
        if check_dataframe(X) and time_index(X):
            resampled_x = X.resample(rule=self.rule).agg(self.aggregation_method)
            return resampled_x

        else:
            return X


class RollingWindow(BaseEstimator,TransformerMixin):
    def __init__(self, window, aggregation_method='mean', center=False, closed=None):
        """
        RollingWindow is a transformer for calculating rolling aggregations for time series data.
        :param window: str, Size of the moving window.
                    1D represents a day
                    1H represents an hour
                    1T represents a minute
                    1S represents a second
                    1L represents a millisecond
                    1U represents a microsecond
                    1N represents a nanosecond

                    different numbers can be placed as prefix eg 2H is 2 hours frequency etc

                    more info here https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

        :param aggregation_method:str, aggregation method, one of mean, std, max, min, sum, var, corr
        :param center: boolean, whether to center the result
        :param closed: one of None, 'right','left','both','neither'
        Usage
        >>> import pandas as pd
        >>> from datamallet.tabular.timeseries import RollingWindow
        >>> price = [10, 11, 9, 13, 14, 18, 17, 19,10, 11, 9, 13, 14, 18, 17, 19,50, 60, 40, 100, 50, 100, 40,10, 11, 9, 13, 14, 18, 17, 19,10,]
        >>> volume = [50, 60, 40, 100, 50, 100, 40, 50,10, 11, 9, 13, 14, 18, 17, 19,50, 60, 40, 100, 50, 100, 40,10, 11, 9, 13, 14, 18, 17, 19,10,]
        >>> d = {'price':price,'volume':volume}
        >>> df = pd.DataFrame(d)
        >>> df['week_starting'] = pd.date_range('01/01/2018',periods=32, freq='1H')
        >>> df.index = df['week_starting']
        >>> df.drop('week_starting', inplace=True, axis=1)

        >>> roller = RollingWindow(window='4H', aggregation_method='max')
        >>> df_r = roller.transform(X=df)
        >>> print(df_r)
                             price  volume
        week_starting
        2018-01-01 00:00:00   10.0    50.0
        2018-01-01 01:00:00   11.0    60.0
        2018-01-01 02:00:00   11.0    60.0
        2018-01-01 03:00:00   13.0   100.0
        2018-01-01 04:00:00   14.0   100.0
        2018-01-01 05:00:00   18.0   100.0
        2018-01-01 06:00:00   18.0   100.0
        2018-01-01 07:00:00   19.0   100.0
        2018-01-01 08:00:00   19.0   100.0
        2018-01-01 09:00:00   19.0    50.0
        2018-01-01 10:00:00   19.0    50.0
        2018-01-01 11:00:00   13.0    13.0
        2018-01-01 12:00:00   14.0    14.0
        2018-01-01 13:00:00   18.0    18.0
        2018-01-01 14:00:00   18.0    18.0
        2018-01-01 15:00:00   19.0    19.0
        2018-01-01 16:00:00   50.0    50.0
        2018-01-01 17:00:00   60.0    60.0
        2018-01-01 18:00:00   60.0    60.0
        2018-01-01 19:00:00  100.0   100.0
        2018-01-01 20:00:00  100.0   100.0
        2018-01-01 21:00:00  100.0   100.0
        2018-01-01 22:00:00  100.0   100.0
        2018-01-01 23:00:00  100.0   100.0
        2018-01-02 00:00:00  100.0   100.0
        2018-01-02 01:00:00   40.0    40.0
        2018-01-02 02:00:00   13.0    13.0
        2018-01-02 03:00:00   14.0    14.0
        2018-01-02 04:00:00   18.0    18.0
        2018-01-02 05:00:00   18.0    18.0
        2018-01-02 06:00:00   19.0    19.0
        2018-01-02 07:00:00   19.0    19.0


        """
        self.window = window
        self.aggregation_method = aggregation_method
        self.center = center
        self.closed = closed
        assert isinstance(window, str), "rule must be a string"
        assert aggregation_method in ['mean','std','min','max','sum','var','corr']
        assert isinstance(center,bool),"center must be a boolean"
        assert closed in [None,'right','left','both','neither']

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.copy()
        if check_dataframe(X) and time_index(X):
            rolling_x = X.rolling(window=self.window,
                                  center=self.center,
                                  axis=0,
                                  closed=self.closed).agg(self.aggregation_method)
            return rolling_x

        else:
            return X
