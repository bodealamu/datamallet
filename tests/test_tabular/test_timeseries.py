import pandas as pd
from datamallet.tabular.timeseries import Resampler, RollingWindow

d = {'price': [10, 11, 9, 13, 14, 18, 17, 19,10, 11, 9, 13, 14, 18, 17, 19,50, 60, 40, 100, 50, 100, 40,10, 11, 9, 13, 14, 18, 17, 19,10,],
     'volume': [50, 60, 40, 100, 50, 100, 40, 50,10, 11, 9, 13, 14, 18, 17, 19,50, 60, 40, 100, 50, 100, 40,10, 11, 9, 13, 14, 18, 17, 19,10,]}
df = pd.DataFrame(d)
df['week_starting'] = pd.date_range('01/01/2018',
                                    periods=32,
                                    freq='1H')
df.index = df['week_starting']
df.drop('week_starting', inplace=True, axis=1)


def test_resampler():
    resampler = Resampler(rule='2H', aggregation_method='mean')
    df_r = resampler.transform(X=df)
    resampler_std = Resampler(rule='2H', aggregation_method='std')
    df_r1 = resampler_std.transform(X=df)
    resampler_min = Resampler(rule='2H', aggregation_method='min')
    df_r2 = resampler_min.transform(X=df)
    resampler_max = Resampler(rule='2H', aggregation_method='max')
    df_r3 = resampler_max.transform(X=df)
    resampler_sum = Resampler(rule='2H', aggregation_method='sum')
    df_r4 = resampler_sum.transform(X=df)
    assert isinstance(df_r, pd.DataFrame)
    assert isinstance(df_r1, pd.DataFrame)
    assert isinstance(df_r2, pd.DataFrame)
    assert isinstance(df_r3, pd.DataFrame)
    assert isinstance(df_r4, pd.DataFrame)
    assert df_r.shape[0]  == 16
    assert df_r1.shape[0] == 16
    assert df_r2.shape[0] == 16
    assert df_r3.shape[0] == 16
    assert df_r4.shape[0] == 16


def test_rollingwindow():
    roller = RollingWindow(window='4H', aggregation_method='max')
    df_r = roller.transform(X=df)
    assert df_r['price'].sum() == 1164.0
