""" purpose: illustrate different methods to forecast time series data
part of a series of lessons taught at Bank of Hawaii, 2017-2018

"""

import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sklearn import linear_model
import math
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint
from statsmodels.tsa.arima_model import ARIMA

# preliminary step - reading and plotting the data
data = pd.read_csv('international-airline-passengers.csv',
                 skiprows=1,
                 skipfooter=3,
                 engine='python',
                 names=['time','passengers'])

plt.plot(data['time'],data['passengers'])
plt.xticks(np.arange(0, data.shape[0], step=23))
plt.show()


#%% Method 1 - linear regression ##############################################

# step 1 - preprocessing
# take the log of the passenger series as it will help us forecast it
# create explanatory variables that can be understood by the model
# ie which month are we in, how many months elapsed since the start
data['passengers_log'] = data['passengers'].apply(lambda x: math.log(float(x)))
data['time'] = data['time'].apply(lambda x: \
                            datetime.datetime.strptime(x,'%Y-%m').date())
data['month'] = data['time'].apply(lambda x: x.month)
data['month_since_start'] = data.index
data['month_since_start_sqr'] = data['month_since_start']**2
data = pd.concat([data,pd.get_dummies(data['month'], prefix ='month')], axis=1)
data = data.drop('month', axis=1)

# step 2 - set apart 36 months of data for testing purposes
data_train = data.loc[data.index[:-36],:]
data_test = data.loc[data.index[-36:],:]
x_train = data_train.drop(['time','passengers','passengers_log'], axis=1)
y_train = data_train['passengers_log']
x_test = data_test.drop(['time','passengers','passengers_log'], axis=1)
y_test = data_test['passengers_log']

# step 3 - train the linear regression model
model = linear_model.LinearRegression()
model.fit(x_train,y_train)

# step 4 - make predictions, store them
y_predict = model.predict(x_test)
data.loc[data.index[-36:],'predict_lin']=np.exp(y_predict)

# step 5 - plot the results
plt.plot(data['time'], data['passengers'])
plt.plot(data['time'], data['predict_lin'])
plt.title('linear regression')
plt.show()

#%% Method 2 - neural network ################################################

# step 1 - redefine y_train and y_test
# the log is not needed any more as neural networks can handle non linear data
y_train = data_train['passengers']
y_test = data_test['passengers']

# step 2 - define the architecture of the model
model = Sequential()
model.add(Dense(28, activation='relu', input_dim=14))
model.add(Dense(28, activation='relu'))
model.add(Dense(1))

# step 3 - define how the model weights will be updated
model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['accuracy'])

# step 4 - define a checkpoint to save the best model
checkpoint = [ModelCheckpoint(filepath='models.hdf5',
                              monitor='loss',
                              mode='min',
                              save_best_only=True)]

# step 5 - train model, load best weights
model.fit(x_train,
          y_train,
          callbacks=checkpoint,
          batch_size=2, 
          epochs=2000, 
          verbose=2)
model.load_weights('models.hdf5')

# step 6 - Make predictions, store them
y_predict = model.predict(x_test)
y_predict = y_predict.reshape(36)
data.loc[ data.index[-36:],'predict_nn'] = y_predict

# step 7 - plot the results
plt.plot(data['time'], data['passengers'])
plt.plot(data['time'], data['predict_nn'])
plt.title('neural network')
plt.show()


#%% Method 3 - time series analysis ###########################################

# step 1 - redefine x_train and x_test 
# No explanatory variables needed - this model uses the lagged values only
# the model requires the index to be the date
train_data=data.loc[ data.index[:-36],['time','passengers']]
train_data['passengers']=train_data['passengers'].apply(float)
train_data=train_data.set_index('time')

# step 2 - create and fit the model 
model = ARIMA(train_data, order=(9,1,1))
model_fit = model.fit()

# step 3 - make predictions, store them 
y_predict = model_fit.forecast(36)
data.loc[ data.index[-36:],'predict_arima'] = y_predict[0]

# step 4 - plot the results
plt.plot(data['time'], data['passengers'])
plt.plot(data['time'], data['predict_arima'])
plt.title('ARIMA')
plt.show()

#%% comparing the models  #####################################################


#using for instance the mean square error as a yardstick
for method in ['predict_lin', 'predict_nn', 'predict_arima']:
    actuals = data.loc[data.index[-24:],'passengers']
    predictions = data.loc[data.index[-24:],method]
    print(method,':', round(np.sqrt(np.mean(np.square(actuals-predictions)))))
