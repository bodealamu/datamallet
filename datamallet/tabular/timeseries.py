from .utils import check_dataframe, time_index
from sklearn.base import BaseEstimator, TransformerMixin


class Resampler(BaseEstimator,TransformerMixin):
    def __init__(self, rule, on=None, aggregation_method='mean'):
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

        :param on:
        :param aggregation_method:
        """
        self.rule = rule
        self.on = on
        self.aggregation_method = aggregation_method

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if check_dataframe(X):
            if time_index(X):
                X.resample(rule=self.rule).agg(self.aggregation_method)

                return X
