# Notes on how to use the pandas library
# The online documentation is wonderful. There are plenty of great blogs and tutorials to learn
# This is meant as a cheatcheet for my colleagues as these are the most common operations in our current positions

import pandas as pd
import numpy as np

# read an excel/csv file
data=pd.read_excel("data.xlsx", sheetname="Sheet1") #sheet_name on more recent pandas versions
data=pd.read_csv("data/data.csv", 
                 skiprows=1, #rows to skip
                 parse_dates=[1], #columns to parse as datetime objects
                 names=["Fare","Date","Distance","Duration"] #new columns names
                 )
# get general info about the dataframe
data.info()
data.describe()

# convert the type of a column
data['Fare'] = data['Fare'].astype(int)

# edit a cell
data.at[1,'Fare']=12 # where 1 is the index

# initialize a new column with 0 values
data['new_column']=0

# creating a column with the quantiles (here deciles) of another column
data['fare_deciles']=pd.qcut(data['Fare'], 10, labels=False)

# you can then export the quantils if you wish
quantiles=data.groupby(by=['fare_deciles']).agg({'Fare':np.max})
quantiles.to_excel('quantiles.xlsx')


# Assign variables to that new column based on simple conditions
data.loc[data['Fare']==0,'new_column']=1

# Assign variables to that new column based on complex conditions
conditions=[(data['Fare']==12 & Data['Distance]>100),
            (data['Fare']==1 & Data['Distance]<=10)]
choices=[4,7]
data['new_column'] = np.select(conditions, choices, default=1)

# normalizing variables
features_to_normalize = ['Distance', 'Duration', 'Fare']
# Store scalings in a dictionary so we can convert back later
scaled_features = {}
for each in features_to_normalize:
    mean, std = data[each].mean(), data[each].std()
    scaled_features[each] = [mean, std]
    data.loc[:, each] = (data[each] - mean)/std

# aggregate variables
nsf=nsf.groupby(by=["Distance","Duration"]).agg({"Fare":"sum"})
nsf=nsf.reset_index()

# one hot encoding
data['Weekday']=data['Date'].apply(lambda x: x.weekday())
data=pd.concat([data, pd.get_dummies(data['Weekday'], prefix='d')], axis=1)
data=data.drop(['Weekday'], axis=1)
                                    
# Split off random 10% of the data for testing
np.random.seed(21)
sample = np.random.choice(data.index, size=int(len(data)*0.9), replace=False)
data, test_data = data.ix[sample], data.drop(sample)

# Split into features and targets
features, targets = data.drop('Target', axis=1), data['Target']
features_test, targets_test = test_data.drop('Target', axis=1), test_data['Target']

# export data to excel
data.to_excel("data.xlsx") 

# export several dataframes df1,df2,df3 to several worksheets
from pandas import ExcelWriter
def save_xls(list_dfs,names, xls_path):
    writer = ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,names[n])
    writer.save()
list_dfs=[df1,df2,df3]
names=['df1','df2','df3']
xls_path="data.xlsx"
save_xls(list_dfs, xls_path) 



