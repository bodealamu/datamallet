# datamallet 
![Screenshot](https://github.com/bodealamu/datamallet/raw/main/datamallet.jpg)

Datamallet is a collection of helpful functions and modules built by Data scientists for Data scientists, to help 
expedite the data science workflow. <br>
From a technical standpoint, datamallet is built on top of the following libraries:<br>
1) Scikit-learn (for creating the transformer classes).
2) Plotly (for the automatic visualization function).
3) Pandas (for creating scikit-learn compatible transformers, 
    and for creating utility functions for wrangling data).
4) Numpy
5) Scipy.

The goal of this project is to help Data scientists become more efficient in their roles by 
providing commonly used functionality that have been battle tested and have been contributed by 
other Data scientists.<br>

## Installation
datamallet is available on pip and can be installed using the command below:<br>

`pip install datamallet ` <br>

## Tests<br>
from the main directory, you can run the tests by simply running the pytest command.<br>

 `pytest`
 

## Quick start<br>
### Automatic Data Visualization
`from datamallet.visualization import AutoPlot`<br>
`import plotly.express as px`<br>
`from datamallet.visualization import AutoPlot`

`tips = px.data.tips()`<br>

`autoplot = AutoPlot(df=tips,include_scatter=True,include_pie=True,include_box=True,
                    include_sunburst=True,
                    include_violin=True,
                    include_treemap=True,
                    include_histogram=True,
                    include_correlation=True,
                    create_html=True,
                    filename='autoplot')`<br>
                    
`list_of_charts = autoplot.show()`<br>

An html file with filename `autoplot.html` would be created (check the current directory, a sample is also 
found in this repo),
the show method also creates a list of the plotly graph objects, so you have the option of not creating the chart but 
using the list of graph objects to display the charts.<br>

`for chart in list_of_charts:`<br>
    `chart.show()`


## Modules
datamallet currently has the following modules
1) `Visualization` module which contains helper functions 
 for automatic visualization and for creating different types of charts such as:<br>
  -Scatter plots.<br>
  -Correlation plots.<br>
  -Histogram.<br>
  -Box plots.<br>
  -Violin plots.<br>
  -Treemaps.<br>
  -Sun burst Charts.<br>
  -Pie Charts.<br>
  -Density Contour Charts.<br>
  -Density Heatmap.<br>
  
  All these charts can be created automatrically using the `Autoplot` class in the visualization module, 
  they can also be created using individual functions in the `plot` module.
  
2) `Tabular` module contains scikit-learn compatible transformers for data manipulation for tabular data,
(data which can be found in a table (pandas dataframe) either pure tabular or timeseries). 
The classes found in the tabular module can be used in a scikit-learn pipeline.<br>
The `Tabular` module contains the following submodules:<br>
  -`features` which contains scikit-learn compatible transformer classes for creating new features
     (more classes are welcome).<br>
  -`timeseries` which contains transformers for manipulating time series data.<br>
  -`utils` which contains helper functions for data wrangling and carrying out checks.<br>
  - `preprocess` which contains transformers for preprocessing data.<br>

<br>




