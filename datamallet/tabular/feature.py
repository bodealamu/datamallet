from sklearn.base import BaseEstimator, TransformerMixin
from .utils import check_columns, check_dataframe, check_numeric


class ColumnAdder(BaseEstimator, TransformerMixin):
    """
    Performs addition of columns
    """
    def __init__(self, column_list, new_column_name):
        """
        Adds columns together in a dataframe and creates a new column

        :param column_list: list of columns to be added together
        :param new_column_name:str, name of new column created from adding the columns in column list together
        """
        self.column_list = column_list
        self.new_column_name = new_column_name
        assert isinstance(column_list,list), "column_list must be a list"
        assert isinstance(new_column_name, str), "new_column_name must be a string"

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if check_dataframe(X) \
                and check_columns(X, self.column_list) \
                and check_numeric(df=X, column_list=self.column_list):
            X[self.new_column_name] = X.loc[:, self.column_list].sum(axis=1)

        return X


class ColumnMultiplier(BaseEstimator,TransformerMixin):
    def __init__(self, column_list, new_column_name):
        """
        Adds columns together and creates a new column

        :param column_list:
        :param new_column_name:
        """
        self.column_list = column_list
        self.new_column_name = new_column_name
        assert isinstance(column_list, list),"column_list must be a list"
        assert isinstance(new_column_name, str), "new_column_name must be a string"

    def fit(self, X, y=None):
        return self

    def transform(self,X, y=None):
        if check_dataframe(X) and \
                check_columns(X, self.column_list) and check_numeric(df=X, column_list=self.column_list):
            X[self.new_column_name] = X.loc[:, self.column_list].prod(axis=1,
                                                                      numeric_only=True,
                                                                      skipna=True)
        return X


class ColumnSubtraction(BaseEstimator, TransformerMixin):
    def __init__(self, left, right, new_column_name):
        """

        :param left:
        :param right:
        :param new_column_name:
        """
        self.left = left
        self.right = right
        self.new_column_name = new_column_name

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if check_dataframe(X) and \
                check_columns(X, [self.left,self.right]) and \
                check_numeric(df=X, column_list=[self.left,self.right]):
            X[self.new_column_name] = X.loc[:, self.left] - X.loc[:, self.right]
        return X


class ExpandingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column_list ,min_periods=1, aggregation_function='sum'):
        """
        Provides functionality for carrying out expanding aggregation
        :param column_list: python list containing column names for which the transformation should be performed on
        :param min_periods: int, minimum number of observations in window required to have a value
        :param aggregation_function: str, aggregation function to be applied, options are 'mean'
               , 'max', 'std' , 'sum', 'min'

        """

        self.column_list = column_list
        self.min_periods = min_periods
        self.aggregation_function = aggregation_function

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if check_columns(column_list=self.column_list) and check_dataframe(X):
            for col in self.column_list:
                X[col] = X[col].expanding(self.min_periods, axis=0).agg(self.aggregation_function)

        return X


class GroupbyTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column_list, aggregation_method='mean'):
        self.column_list = column_list
        self.aggregation_method = aggregation_method

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if check_dataframe(df=X) and check_columns(df=X, column_list=self.column_list):
            X = X.groupby(self.column_list).agg(self.aggregation_method)

            return X


