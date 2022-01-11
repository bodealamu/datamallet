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
        # self.on = on
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
