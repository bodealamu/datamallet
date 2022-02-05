import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from .utils import (check_columns,
                    check_dataframe,)


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




