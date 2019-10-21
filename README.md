#NUI_Projection



This is a Python2.7 Package used to project NUI discoveries respecting sample sizes.

url: https://github.com/WalfredMA/NUI_Projection

The details for the methodology and mathematical reasoning can be found in ./NUI_projection_reasoning.pdf if interested.




Requirements
--------------------------------

1. Python2.7

2. Scipy 1.20 or higher



Installation
--------------------------------

1.Install via local files:

$ cd $file_directory

$ pip install


2.Install via PyPi:

$ pip install -i https://test.pypi.org/simple/ NUI-projection==0.0.2




Usages 
--------------------------------

Please use this package in python2.7 scripts.

First import this package by:
>>>from NUI_projection import *

There are two functions in this package:




1. downsample

Used to downsample current dataset to lower sample sizes. Output is a pandas dataframe with header indicates sample sizes and index indicates number of NUIs at certain sample count. 

>>> downsample(allcounts=[3,2,2,4,4,6,4,4,5,6,2,4,5,6,6], current_size=6, outfile=./save_downsample.csv)

     6         5    4     3         2
2  3.0  2.500000  3.8  5.05  7.733333
3  1.0  3.833333  4.2  6.05       NaN
4  5.0  3.333333  5.0   NaN       NaN
5  2.0  4.333333  NaN   NaN       NaN
6  4.0       NaN  NaN   NaN       NaN

Attributes:

allcounts [list];  a list of NUI sample counts. For example, if there are three NUI and each shared by two samples, allcounts=[2,2,2]

current_size [int]; a integer gives the sample size of the current dataset.

(optional) outfile [string]; a string path to save down-sampling data frame to a csv file , which has a header indicates downsampled sample size while each row indicates number of NUI from sample count = 2 to current_size. 






2. projection

Used to project current dataset to higher sample sizes. Output: a python dict of float numbers indicates expected total non-redundant NUI found from sample size 2 ~ project_size.

>>> projection(allcounts=[3,2,2,4,4,6,4,4,5,6,2,4,5,6,6], current_size=6, project_size)
{2: 7.7333333333333325, 3: 11.099999999999998, 4: 13.0, 5: 13.999999999999996, 6: 15.0, 7: 14.077785373084197, 8: 12.72647510387041, 9: 11.041423570684977, 10: 9.0893788383563319}


Attributes:

allcounts [list];  the same with downsample

current_size [int]; the same with downsample

project_size [int]; the maximum up-projection sample size. 




Support
--------------------------------

If you are having question, please let us know.
Email: Wangfei.MA@ucsf.edu 




License
--------------------------------

The project is licensed under the MIT License.

Can be also found in PyPi as NUI_projection.
