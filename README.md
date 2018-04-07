# snippets
A collection of snippets illustrating (not showcasinng best practices) various technique of data manipulation in python.Project created as part of a series of lessons taught at Bank of Hawaii in 2017-2018. 

# Python versions requirements
- python 2.7.9 for the Google Cloud Platform
- python 3.5 for the regressions 

# Python packages requirements
- pandas
- matplotlib
- seaborn
- scikit-learm
- h5py
- keras
- scipy
- statsmodel
- datetime
- math
- numpy


# Other requirements
the regression, matplotlib and pandas snippet make use of the international passengers dataset. It can be downloaded here:
https://datamarket.com/data/set/22u3/international-airline-passengers-monthly-totals-in-thousands-jan-49-dec-60#!ds=22u3&display=line

# Usage
You'll find in it the essentials tools to:
- manipulate data with pandas
- make simple plots with matplotlib
- make regressions with sklearn, statsmodel, or keras
- find which probability distribution best fits an observed sample of values
- adapt a web application to the Google Cloud Platform

# Notes on the regressions
The 3 models shown illustrate 3 different ways of predicting time series. In a nutshell:
- linear regression: we guess what factors influence the value to predict.
We find the polynomial function taking the explanatory variables as arguments which best matches the observed values. 
One specific advantage is the ability to check the function parameters to see which factors count most. 
- neural network: we also guess what factors influence the value to predict.
We create a very complex function and tweak it little by little to that minimises the error. 
In theory, if any function can be approached by a neural network so we can find the best possible function - although it would take a lot of trials and errors.
- ARIMA: we call a model that observes the trend and the seasonality, then prolongates the curve. 
One specific advantage is the simplicity - no explanatory variables are needed. 

