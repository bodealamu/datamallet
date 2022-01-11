import pandas as pd
from datamallet.visualization import AutoPlot

df = pd.DataFrame({'A':[1,2,3,4,5],
                   'B':[2,4,6,8,10],
                   'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female'],
                   'E':[True,True,False,True,True]})

df2 = pd.DataFrame({'C':['dog','cat', 'sheep','dog','cat'],
                   'D':['male','male','male','female','female']})

df3 = pd.DataFrame({'A':[1,1,2,1,1],
                   'B':[2,2,1,2,0],})

df4 = pd.DataFrame({'Age':[1,2,3,4,5],
                   'Gender':['Male','Female','Unknown','Male','Female'],
                    'City':['austin', 'austin', 'lagos','abuja', 'ibadan']
                   })


def test_autoplot():
    autoplot = AutoPlot(df=df2)
    assert len(autoplot.chart_type()) == 0, "No numeric columns in dataframe"
    assert isinstance(autoplot.show(), list)
    autoplot1 = AutoPlot(df=df3)
    chart_type = autoplot1.chart_type()
    assert len(chart_type) != 0
    assert isinstance(autoplot1.show(), list)
    assert 'scatter' in chart_type
    assert 'correlation_plot' in chart_type
    autoplot2 = AutoPlot(df=df4,include_scatter=True)
    chart_type2 = autoplot2.chart_type()
    assert 'correlation_plot' not in chart_type2
    assert 'scatter' not in chart_type2, "scatter plot needs at a minimum 2 numeric columns"
    assert 'timeseries_plot' not in chart_type2, "no time series index"
