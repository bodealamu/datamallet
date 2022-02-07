from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from .utils import (check_columns,
                    percentage_missing,
                    extract_numeric_cols,
                    column_mean, check_numeric)
from datamallet.tabular.utils import check_dataframe, check_dictionary


class NADropper(BaseEstimator, TransformerMixin):
    def __init__(self, axis=1,how='all',thresh=None):
        """
        Transformer for dropping columns or rows with missing value.
        :param axis: 0 or 'index', drops rows which contain missing value, 1 or 'columns' drops columns which contain missing value.
        :param how: str, 'any','all'. drop row or column if any NA is present, drop row or column if all values are missing.
        :param thresh: int, require that many non NA values

        Usage
        >>> import pandas as pd
        >>> import numpy as np
        >>> df3 = pd.DataFrame({'A':[np.nan,2,3,4,5],'B':[2,np.nan,np.nan,np.nan,10],
            ... 'C':['dog','cat', 'sheep','dog','cat'],'D':['male','male','male','female','female'],
            ... 'E':[True,True,False,True,True]})
        >>> nadropper = NADropper(axis='columns', how='any')
        >>> droped2 = nadropper.transform(X=df2)
               C       D      E
        0    dog    male   True
        1    cat    male   True
        2  sheep    male  False
        3    dog  female   True
        4    cat  female   True

        """
        self.axis = axis
        self.how = how
        self.thresh = thresh
        assert isinstance(thresh,int) or thresh is None,"thresh is expected to be an integer"
        assert how in ['any','all']
        assert axis in [0,1,'index','columns'],""

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if check_dataframe(df=X):
            X = X.copy()
            X.dropna(axis=self.axis, how=self.how, thresh=self.thresh, inplace=True)

        return X


class DropPercentageMissing(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=50):
        """
        Drops column which have a percentage of missing value greater than or equal to the threshold
        :param threshold: int

        Usage
         >>> import pandas as pd
        >>> from datamallet.tabular.imputation import DropPercentageMissing
        >>> df = pd.DataFrame(dict(age=[5, 6, np.NaN],born=[pd.NaT, pd.Timestamp('1939-05-27'),pd.Timestamp('1940-04-25')],
        ... name=['Alfred', 'Batman', ''],toy=[None, 'Batmobile', 'Joker']))
        >>> bn = DropPercentageMissing(threshold=20).transform(X=df)
        >>> print(bn)
             name
        0  Alfred
        1  Batman
        2

        """
        assert isinstance(threshold, int)
        self.threshold = threshold

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X = X.copy()
        percentage_mis_dict = percentage_missing(df=X)
        drop_list = list()

        for column, percentage in percentage_mis_dict.items():
            if percentage >= self.threshold:
                drop_list.append(column)

        X.drop(axis='columns', inplace=True,labels=drop_list)

        return X


class ConstantValueFiller(BaseEstimator, TransformerMixin):
    def __init__(self, value, limit=None):
        """
        Performs Missing value imputation using a constant value or dictionary,
        this dictionary has the column name as key and the value to use to fill as value
        :param value:  dictionary which maps column name to value or interger or string
        :param limit:int, (default = None) the maximum number of missing value per column to be filled,
                if None, all missing values would be filled

        Usage
        >>> import pandas as pd
        >>> import numpy as np
        >>> df2 = pd.DataFrame({'A':[np.nan,2,3,4,5,8],'B':[2,np.nan,np.nan,np.nan,10,9],'C':[1,3,5, np.nan, np.nan,7]})
        >>> cvf = ConstantValueFiller(value={'A':100, 'B':200,'C':300}, limit=1)
        >>> vx = cvf.transform(X=df2)
        >>> print(vx)
               A      B      C
        0  100.0    2.0    1.0
        1    2.0  200.0    3.0
        2    3.0    NaN    5.0
        3    4.0    NaN  300.0
        4    5.0   10.0    NaN
        5    8.0    9.0    7.0

        >>> cvf = ConstantValueFiller(value=200, limit=None)
        >>> vx = cvf.transform(X=df2)
        >>> print(vx)
               A      B      C
        0  200.0    2.0    1.0
        1    2.0  200.0    3.0
        2    3.0  200.0    5.0
        3    4.0  200.0  200.0
        4    5.0   10.0  200.0
        5    8.0    9.0    7.0
        """
        self.value = value
        self.limit = limit
        assert isinstance(value, dict) or value is not None, "fill_dict is expected to be a dictionary"
        assert isinstance(limit, int) or limit is None

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.copy()

        if check_dataframe(df=X):
            if isinstance(self.value, int) or isinstance(self.value, float) or isinstance(self.value, str):
                X.fillna(value=self.value, inplace=True, limit=self.limit)
                return X
            if check_dictionary(df=X, column_dict=self.value):
                X.fillna(value=self.value, inplace=True, limit=self.limit)
                return X

        return X


class NaFiller(BaseEstimator, TransformerMixin):
    def __init__(self,column_list=None,
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
          >>> from datamallet.tabular.imputation import NaFiller
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