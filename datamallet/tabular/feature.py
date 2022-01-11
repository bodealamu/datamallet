from sklearn.base import BaseEstimator, TransformerMixin
from .utils import check_columns, check_dataframe, check_numeric


class ColumnAdder(BaseEstimator, TransformerMixin):
    """
    Performs addition of columns
    """
    def __init__(self, column_list, new_column_name):
        """
        Adds columns together in a dataframe and creates a new column

        :param column_list: list of columns to be added together, they must all be numeric columns
        :param new_column_name:str, name of new column created from adding the columns in column list together

        Usage
        >>> import pandas as pd
        >>> from datamallet.tabular.feature import ColumnAdder
        >>> df = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'C':['dog','cat', 'sheep','dog','cat'],'D':['male','male','male','female','female'],'E':[True,True,False,True,True]})

        >>> column_adder = ColumnAdder(column_list=['A','B'],new_column_name='Z')
        >>> added_df = column_adder.transform(X=df)
        >>> print(added_df)

           A   B      C       D      E   Z
        0  1   2    dog    male   True   3
        1  2   4    cat    male   True   6
        2  3   6  sheep    male  False   9
        3  4   8    dog  female   True  12
        4  5  10    cat  female   True  15


        """
        self.column_list = column_list
        self.new_column_name = new_column_name
        assert isinstance(column_list,list), "column_list must be a list"
        assert isinstance(new_column_name, str), "new_column_name must be a string"

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if check_dataframe(X) \
                and check_numeric(df=X, column_list=self.column_list):
            X = X.copy()
            X[self.new_column_name] = X.loc[:, self.column_list].sum(axis=1)

        return X


class ColumnMultiplier(BaseEstimator,TransformerMixin):
    def __init__(self, column_list, new_column_name):
        """
        Adds columns together and creates a new column

        :param column_list:list of columns to be multiplied together, they must all be numeric columns
        :param new_column_name:str, name of new column created from adding the columns in column list together

        Usage
        >>> import pandas as pd
        >>> from datamallet.tabular.feature import ColumnMultiplier
        >>> df3 = pd.DataFrame({'A':[1,1,2,1,1],'B':[2,2,1,2,0],})
        >>> multiplied_df = ColumnMultiplier(column_list=['A','B'], new_column_name='Z').transform(X=df3)
        >>> print(multiplied_df)
           A  B  Z
        0  1  2  2
        1  1  2  2
        2  2  1  2
        3  1  2  2
        4  1  0  0


        """
        self.column_list = column_list
        self.new_column_name = new_column_name
        assert isinstance(column_list, list),"column_list must be a list"
        assert isinstance(new_column_name, str), "new_column_name must be a string"

    def fit(self, X, y=None):
        return self

    def transform(self,X, y=None):
        if check_dataframe(X) and \
                 check_numeric(df=X, column_list=self.column_list):
            X = X.copy()
            X[self.new_column_name] = X.loc[:, self.column_list].prod(axis=1,
                                                                      numeric_only=True,
                                                                      skipna=True)
        return X


class ColumnSubtraction(BaseEstimator, TransformerMixin):
    def __init__(self, left, right, new_column_name):
        """

        :param left: name of column on the left side of the minus side
        :param right: name of column on the right side of the minus side
        :param new_column_name:str, name of new column

        Usage
        >>> import pandas as pd
        >>> from datamallet.tabular.feature import ColumnSubtraction
        >>> df3 = pd.DataFrame({'A':[1,1,2,1,1],'B':[2,2,1,2,0],})
        >>> subtracted_df = ColumnSubtraction(left='A', right='B', new_column_name='C').transform(df3)
        >>> print(subtracted_df)
           A  B  C
        0  1  2 -1
        1  1  2 -1
        2  2  1  1
        3  1  2 -1
        4  1  0  1

        """
        self.left = left
        self.right = right
        self.new_column_name = new_column_name
        assert isinstance(left,str), "left must be a string with name of column"
        assert isinstance(right, str), "right must be a string with name of column"
        assert isinstance(new_column_name, str), "new_column_name must be a string"

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if check_dataframe(X) and \
                check_numeric(df=X, column_list=[self.left,self.right]):
            X = X.copy()
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

        Usage
        >>> import pandas as pd
        >>> from datamallet.tabular.feature import ExpandingTransformer
        >>> df = pd.DataFrame({"B": [0, 1, 2, np.nan, 4], "A": [0, 1, 0, np.nan, 4]})
        >>> expander = ExpandingTransformer(column_list=['B'],min_periods=2,aggregation_function='sum')
        >>> df_new = expander.transform(X=df)
        >>> print(df_new)
             B    A
        0  NaN  0.0
        1  1.0  1.0
        2  3.0  0.0
        3  3.0  NaN
        4  7.0  4.0

        """

        self.column_list = column_list
        self.min_periods = min_periods
        self.aggregation_function = aggregation_function
        assert isinstance(column_list, list)
        assert isinstance(min_periods, int)
        assert aggregation_function in ['mean','max','std','sum','min']

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if check_columns(column_list=self.column_list, df=X) and check_dataframe(X):
            X = X.copy()
            for col in self.column_list:
                X[col] = X[col].expanding(self.min_periods, axis=0).agg(self.aggregation_function)

        return X


class GroupbyTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column_list, aggregation_method='mean'):
        """

        :param column_list:list of column names to be used for the aggregation (groupin)
        :param aggregation_method:str, aggregation method, one of 'sum','mean','std'

        Usage
        >>> import pandas as pd
        >>> from datamallet.tabular.feature import GroupbyTransformer
        >>> df4 = pd.DataFrame({'Age':[1,2,3,4,5],
                   'Gender':['Male','Female','Unknown','Male','Female'],
                    'City':['austin', 'austin', 'lagos','abuja', 'ibadan']
                   })
        >>> grouped_df = GroupbyTransformer(column_list=['Gender', 'City'], aggregation_method='mean').transform(df4)

        >>> print(grouped_df)

                        Age
        Gender  City
        Female  austin    2
                ibadan    5
        Male    abuja     4
                austin    1
        Unknown lagos     3

        >>> grouped_df = GroupbyTransformer(column_list=['Gender'], aggregation_method='sum').transform(df4)

        >>> print(grouped_df)

                 Age
        Gender
        Female     7
        Male       5
        Unknown    3


        """
        self.column_list = column_list
        self.aggregation_method = aggregation_method
        assert isinstance(column_list, list)
        assert aggregation_method in ['mean', 'std', 'sum']

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if check_dataframe(df=X) and check_columns(df=X, column_list=self.column_list):
            X = X.copy()
            X = X.groupby(self.column_list).agg(self.aggregation_method)

            return X


