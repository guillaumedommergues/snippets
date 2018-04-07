
# purpose: illustrate how to quickly plot data with matplotlib
# part of a series of lessons taught at Bank of Hawaii, 2017-2018

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
# pyplot doc here: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.html

#%%############################################################################
###################### data preparation #######################################
###############################################################################

# read a file
df=pd.read_csv('international-airline-passengers.csv',
               names=['time','passengers'],
               skiprows=1,
               skipfooter=3,
               engine='python')

# adding variables
df['time']=df['time'].apply(lambda x: datetime.strptime(x,'%Y-%m'))
df['year']=df['time'].apply(lambda x: x.year)
df['month']=df['time'].apply(lambda x: x.month)
df['month_str']=df['time'].apply(lambda x: x.strftime('%b'))
df['season']='spring'
df.loc[df['month'].isin([6,7,8]),'season']='summer'
df.loc[df['month'].isin([9,10,11]),'season']='fall'
df.loc[df['month'].isin([12,1,2]),'season']='winter'

# creating a new dataframe with 2 years of data
df_1959=df.loc[df['year']==1959,['month','passengers']]
df_1960=df.loc[df['year']==1960,['month','passengers']]
df_1959=df_1959.rename(columns={'passengers':'59'})
df_1960=df_1960.rename(columns={'passengers':'60'})
df_1959_60=pd.merge(df_1959,df_1960, on='month', how='outer')

# creating a new dataframe averages by season
df_season=df.groupby('season').agg({'passengers':'mean'})

#%%############################################################################
###################### basic plotting #########################################
###############################################################################

# line chart
plt.plot(df['time'],df['passengers'])
plt.show()

# pie chart
plt.pie(df_season['passengers'])
plt.show()

# histogram
plt.hist(df['passengers'])
plt.show()

# bar chart
plt.bar(df_1959_60['month'],df_1959_60['60'])
plt.show()

# multiple plots in one chart
plt.bar(df_1959_60['month'],df_1959_60['59'], width=-0.3, align='edge')
plt.bar(df_1959_60['month'],df_1959_60['60'], width=0.3, align='edge')
plt.show()

# mixed plot
plt.plot(df_1959_60['month'],df_1959_60['59'])
plt.bar(df_1959_60['month'],df_1959_60['60'])
plt.show()

# several plots in one figure
# (2,1,1) means 'make a figure with a 2x1 grid, put subplot in 1st box'
# (2,1,2) means 'make a figure with a 2x1 grid, put subplot in 2nd box' ... etc
plt.figure()
plt.subplot(2,1,1)
plt.plot(df_1959_60['month'],df_1959_60['59'])
plt.subplot(2,1,2)
plt.bar(df_1959_60['month'],df_1959_60['60'])
plt.show()

# save a plot
plt.plot(df['time'],df['passengers'])
plt.savefig('plot.png')

#%%
###############################################################################
###################### adding formatting ######################################
###############################################################################

# custom formatting
plt.figure(figsize=(6,4))
plt.plot(df_1959_60['month'],
         df_1959_60['59'],
         label='prior year',
         color='#004D40',
         linewidth=3,
         linestyle="--")
plt.bar(df_1959_60['month'],
        df_1959_60['60'],
        label='current year',
        color='#004D40',
        alpha=0.5,
        width=0.8)
plt.xticks(range(0,12))
plt.ylim([0,1000])
plt.title('recent trends')
plt.legend()
plt.show()

# more formatting on subplot
plt.figure(figsize=(6,6))
plt.suptitle('Monthly International Passengers Counts\n\
            short/long term trends') #overarching title
plt.subplot(2,1,1)
plt.plot(df['time'],df['passengers'])
plt.subplot(2,1,2)
plt.bar(df_1959_60['month'],df_1959_60['60'])
plt.xticks(range(1,13))
plt.subplots_adjust(top=0.9) #leavs 10% of the space for title
plt.show()
#%%
# canned formatting with seaborn
sns.set()
plt.plot(df_1959_60['month'],df_1959_60['59'])
plt.bar(df_1959_60['month'],df_1959_60['60'])
plt.show()

#%%
###############################################################################
###################### beyond pyplot ##########################################
###############################################################################

# A matplotlib object is made of a Figure (top level container object), Axes 
# (what is usually refereed to as a "plot"), Axis (the x and y axes), and 
# Artists (lin3es, boxes, etc) object
# matplotlib.pyplot is a shortcut to apply function to these objects, however
# we sometimes need to manipulate the Figure or Axis object with the 
# gcf (get current Figure) and gca (get current Axes) functions

# example - two line charts on linear vs log scale
plt.plot(df['time'],df['passengers'],color='blue',label='linear scale')
plt.legend(loc='upper left')
ax1=plt.gca()
ax2=plt.twinx()
ax2.plot(df['time'],df['passengers'],color='green',label='log scale')
ax2.set_yscale('log')
plt.legend(loc='upper right')
