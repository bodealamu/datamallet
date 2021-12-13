import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from .utils import check_columns, check_dataframe, column_mean


class ColumnDropper(BaseEstimator, TransformerMixin):
    def __init__(self,
                 column_list):
        """
        This class drops columns from a dataframe, this operation is done inplace.

        :param column_list: list which contains the names of columns in the dataframe

        """
        self.column_list = column_list

    def fit(self, X, y=None):
        assert (isinstance(X, pd.DataFrame)), 'X needs to be a pandas dataframe'
        return self

    def transform(self, X, y=None):
        if check_columns(X, self.column_list) and check_dataframe(X):
            X.drop(labels=self.column_list, inplace=True, axis=1)
        return X


class NaFiller(BaseEstimator, TransformerMixin):
    """
      Transformer for filling missing values using various methods or values

      :param value: float, int or dictionary which contains values to be used for filling values
                      , only prvide if method is None
      :param method: str, method for use with filling missing value, current values allowed are
                      bfill for backfilling
                      ffill for forward filling
                      mean for filling with the average values for each column
      :param limit:int, default = None, the maximum number of missing values to be filled
      """
    def __init__(self,
                 value=None,
                 method=None,
                 limit=None):

        self.value = value
        self.method = method
        self.limit = limit

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df_check = check_dataframe(X)
        if self.method == 'bfill' and df_check:
            X.fillna(method='bfill', inplace=True, limit=self.limit)

        if self.method == 'ffill' and df_check:
            X.fillna(method='ffill', inplace=True, limit=self.limit)

        if self.method == 'mean' and df_check:
            X.fillna(value=column_mean(df=X), inplace=True)

        if self.method is None and df_check and self.value is not None:
            X.fillna(value=self.value, inplace=True)

        return X


class ColumnRename(BaseEstimator, TransformerMixin):
    def __init__(self, rename_dictionary):
        """
        Rename columns in place
        :param rename_dictionary: python dictionary with the old names as keys and new names as value.
        """
        self.rename_dictionary = rename_dictionary

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        assert isinstance(self.rename_dictionary, dict), 'Rename dictionary must be a dictionary'

        col_list = list()
        for old_name, new_name in self.rename_dictionary.items():
            col_list.append(old_name)

        if check_columns(df=X, column_list=col_list) and check_dataframe(df=X):
            X.rename(columns=self.rename_dictionary, inplace=True)

        return X






