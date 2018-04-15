
# purpose: illustrate some common pandas operations to manipulate tabular data
# part of a series of lessons taught at Bank of Hawaii, 2017-2018

from __future__ import division
import pandas as pd
import numpy as np
from datetime import datetime
#%%

# read a file
df = pd.read_csv('international-airline-passengers.csv',skipfooter=3)

# print the first and last lines
df.head()
df.tail()

# get general info about the dataframe  
df.info()  
df.describe() 

# print the column names
df.columns

# find the count of rows/columns
nrows = df.shape[0]
ncols = df.shape[1]

# rename the columns
df = df.rename(
        columns={'Month':'time',
                 'International airline passengers: monthly totals in thousands. Jan 49 ? Dec 60':'passengers'
                 }
        )

# convert the type of a column
df['passengers'] = df['passengers'].astype(float)

# edit one value
df.at[0,'passengers'] = 200

# calculate some summary data
psg_min = df['passengers'].min()
psg_max = df['passengers'].max()
psg_mean = df['passengers'].mean()
psg_std_dev = df['passengers'].std()

# create a column with simple calculations 
df['psg_normalized'] = (df['passengers']-psg_mean)/psg_std_dev

# create a column column based on if/else calculation 
df['500+'] = False
df.loc[df['passengers'] >= 500,'500+'] = True

# create new columns by applying a function 
df['psg_min_max_scaled'] = df['passengers'].apply(lambda x:\
  (x-psg_min)/(psg_max-psg_min))

#create a column with deciles
df['deciles'] = pd.qcut(df['passengers'], 10, labels=False)

# create a new dataframe based on cell values/column names
df_500 = df.loc[df['500+'],:]  #or df_500_scaled=df.loc[df['passengers']>=500,:]
df_scaled = df.loc[:,['psg_normalized','psg_min_max_scaled']]

# create a new dataframe based on row/column index
df_first_10 = df.iloc[range(0,10),[2,3]]

# randomly keep 90% of the data for train, 10% for test
np.random.seed(0) #for reproductability
sample = np.random.choice(df.index, size=int(len(df)*0.9), replace=False)  
df_train, df_test = df.iloc[sample], df.drop(sample) 

# remove a column
df = df.drop('psg_min_max_scaled', axis=1) 

# aggregate data based on a criteria
df['month'] = df['time'].apply(lambda x:datetime.strptime(x,'%Y-%m'))
df['month'] = df['month'].apply(lambda x:x.month)
avg_by_month = df.groupby(['month']).agg({'passengers':'mean'})

# change the index
df = df.set_index('time')

# export the data
avg_by_month.to_csv('averages.csv')


