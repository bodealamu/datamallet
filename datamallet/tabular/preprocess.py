import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from .utils import (check_columns,
                    extract_numeric_cols,
                    check_dictionary,
                    check_dataframe,
                    column_mean,
                    check_numeric)


class ColumnDropper(BaseEstimator, TransformerMixin):
    def __init__(self,
                 column_list):
        """
        This class drops columns from a dataframe, this operation is done inplace.

        :param column_list: list which contains the names of columns in the dataframe to be dropped

        Usage
        >>> from datamallet.tabular.preprocess import ColumnDropper
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female'],
                   'E':[True,True,False,True,True]})

        # initialize the ColumnDropper class
        >>> column_dropper = ColumnDropper(column_list=['C','D','E'])

        # call the transform method
        >>> dropped_df = column_dropper.transform(X=df)

        # check
        >>> print(dropped_df.columns)
        Index(['A', 'B'], dtype='object')

        """
        self.column_list = column_list

    def fit(self, X, y=None):
        assert (isinstance(X, pd.DataFrame)), 'X needs to be a pandas dataframe'
        return self

    def transform(self, X, y=None):
        if check_columns(X, self.column_list) and check_dataframe(X):
            X = X.copy()
            X.drop(labels=self.column_list, inplace=True, axis=1)
        return X


class NaFiller(BaseEstimator, TransformerMixin):
    def __init__(self,column_list,
                 method='mean',
                 limit=None,
                 ):
        """
          Transformer for filling missing values using various methods or values

          :param value: float, int or dictionary which contains values to be used for filling values
                          , only provide if method is None
          :param method: str, method for use with filling missing value, current values allowed are
                          bfill for backfilling
                          ffill for forward filling
                          mean for filling with the average values for each column
          :param limit:int, default = None, the maximum number of missing values to be filled
          :param column_list:, list, default is None, list of column names to apply the imputation to

          Usage
          # using method = bfill
          >>> import pandas as pd
          >>> import numpy as np
          >>> from datamallet.tabular.preprocess import NaFiller
          >>> df2 = pd.DataFrame({'A':[np.nan,2,3,4,5,8],'B':[2,np.nan,np.nan,np.nan,10,9],'C':[1,3,5,np.nan,np.nan,7]})
          >>> print(df2)
               A     B    C
            0  NaN   2.0  1.0
            1  2.0   NaN  3.0
            2  3.0   NaN  5.0
            3  4.0   NaN  NaN
            4  5.0  10.0  NaN
            5  8.0   9.0  7.0
          >>> nafiller = NaFiller( method='bfill', limit=None, column_list=None)
          >>> cx = nafiller.transform(X=df2)
          >>> print(cx)
               A     B    C
            0  2.0   2.0  1.0
            1  2.0  10.0  3.0
            2  3.0  10.0  5.0
            3  4.0  10.0  7.0
            4  5.0  10.0  7.0
            5  8.0   9.0  7.0

            # Using ffill
          >>> nafiller = NaFiller( method='ffill', limit=None, column_list=None)
          >>> cx = nafiller.transform(X=df2)
          >>> print(cx)
               A     B    C
            0  NaN   2.0  1.0
            1  2.0   2.0  3.0
            2  3.0   2.0  5.0
            3  4.0   2.0  5.0
            4  5.0  10.0  5.0
            5  8.0   9.0  7.0

          >>> nafiller = NaFiller( method='mean', limit=None, column_list=None)
          >>> cx = nafiller.transform(X=df2)
          >>> print(cx)
              A     B    C
          0  4.4   2.0  1.0
          1  2.0   7.0  3.0
          2  3.0   7.0  5.0
          3  4.0   7.0  4.0
          4  5.0  10.0  4.0
          5  8.0   9.0  7.0

          >>> d = pd.DataFrame({'A':[np.nan,2,3,4,5,8],'B':[2,np.nan,np.nan,np.nan,10,9],'C':[1,3,5, np.nan, np.nan,7],'D':[4,np.nan,np.nan, np.nan, np.nan,7]})
          >>> nafiller = NaFiller( method='mean', column_list=['B','C'], limit=1)
          >>> cx = nafiller.transform(X=d)
               A     B    C    D
           0  NaN   2.0  1.0  4.0
           1  2.0   7.0  3.0  NaN
           2  3.0   NaN  5.0  NaN
           3  4.0   NaN  4.0  NaN
           4  5.0  10.0  NaN  NaN
           5  8.0   9.0  7.0  7.0


        """

        self.method = method
        self.limit = limit
        self.column_list = column_list
        assert method in ['bfill', 'ffill','mean']
        assert isinstance(limit, int) or limit is None
        assert isinstance(column_list,list) or column_list is None

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X = X.copy()

        if self.method == 'bfill':
            if isinstance(self.column_list, list) and check_columns(df=X,column_list=self.column_list):
                for col in self.column_list:
                    X[col] = X[col].fillna(method='bfill', limit=self.limit)
                return X
            elif self.column_list is None:
                X.fillna(method='bfill', inplace=True, limit=self.limit)
                return X
            else:
                return X

        if self.method == 'ffill':
            if isinstance(self.column_list, list) and check_columns(df=X,column_list=self.column_list):
                for col in self.column_list:
                    X[col] = X[col].fillna(method='ffill', limit=self.limit)
                return X
            elif self.column_list is None:
                X.fillna(method='ffill', inplace=True, limit=self.limit)
                return X
            else:
                return X

        if self.method == 'mean':

            if isinstance(self.column_list, list) and check_numeric(df=X,column_list=self.column_list):
                X.fillna(value=column_mean(df=X, column_list=self.column_list), inplace=True,limit=self.limit)
                return X
            if self.column_list is None:
                numeric_cols = extract_numeric_cols(df=X)

                # if no columns are specified, use only numeric columns
                X.fillna(value=column_mean(df=X, column_list=numeric_cols), inplace=True, limit=self.limit)
                return X


class ConstantValueFiller(BaseEstimator, TransformerMixin):
    def __init__(self, fill_dict, limit=None):
        """
        Performs Missing value imputation using a dictionary,
        this dictionary has the column name as key and the value to use to fill as value
        :param fill_dict: dict, dictionary which maps column name to value
        :param limit:int, (default = None) the maximum number of missing value per column to be filled,
                if None, all missing values would be filled

        Usage
        >>> import pandas as pd
        >>> import numpy as np
        >>> df2 = pd.DataFrame({'A':[np.nan,2,3,4,5,8],'B':[2,np.nan,np.nan,np.nan,10,9],'C':[1,3,5, np.nan, np.nan,7]})
        >>> cvf = ConstantValueFiller(fill_dict={'A':100, 'B':200,'C':300}, limit=1)
        >>> vx = cvf.transform(X=df2)
        >>> print(vx)
               A      B      C
        0  100.0    2.0    1.0
        1    2.0  200.0    3.0
        2    3.0    NaN    5.0
        3    4.0    NaN  300.0
        4    5.0   10.0    NaN
        5    8.0    9.0    7.0
        """
        self.fill_dict = fill_dict
        self.limit = limit
        assert isinstance(fill_dict, dict), "fill_dict is expected to be a dictionary"
        assert isinstance(limit, int) or limit is None

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.copy()

        if check_dictionary(df=X, column_dict=self.fill_dict) and check_dataframe(df=X):
            X.fillna(value=self.fill_dict, inplace=True, limit=self.limit)

        return X


class ColumnRename(BaseEstimator, TransformerMixin):
    def __init__(self, rename_dictionary):
        """
        Rename columns in place
        :param rename_dictionary: python dictionary with the old names as keys and new names as value.

        Usage
        >>> from datamallet.tabular.preprocess import ColumnRename
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A':[1,2,3,4,5],'B':[2,4,6,8,10],'D':['male','male','male','female','female'],'E':[True,True,False,True,True]})

        >>> rename_dictionary={'A':'V','B':'W'}

        >>> columnrenamer = ColumnRename(rename_dictionary=rename_dictionary)
        >>> renamed_df = columnrenamer.transform(X=df)

        >>> print(renamed_df.columns)
        Index(['V', 'W', 'C', 'D', 'E'], dtype='object')

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
            X = X.copy()
            X.rename(columns=self.rename_dictionary, inplace=True)

        return X






