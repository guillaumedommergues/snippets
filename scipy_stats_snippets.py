# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 09:03:26 2018

@author: 58103
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

#%%
# randomly generate data following a probability distribution - here uniform
data=st.uniform.rvs(loc=0,scale=1,size=100)
# plot the data
plt.hist(data, bins=10, normed=True)
# plot the distribution
x_data=np.linspace(0,1,11)
pdf=st.uniform.pdf(x=x_data, loc=0, scale=1 )
plt.plot(x_data, pdf)
plt.xlim([0,1])
plt.show()

#%%
# repeat the experience 100 times and store the sum of the results
data_repeat=[st.uniform.rvs(loc=0,scale=1,size=1000).sum() for _ in range(0,100)]    
# let's see which distribution best represents this experience
# the central limit theorem proves that the distribution will tend to be normal
# if we repeat it enough times. Is it true for a small sample of 100 repeats?
# let's create the empirical cumulative distribution function 
# try a few known distributions
# and see which one is the closest by comparing the mean squared error

# Step 1 - create the empirical cumulative distribution function
x_observed, y_observed=np.unique(data_repeat, return_counts=True)
y_observed_normed=y_observed/np.sum(y_observed)
y_observed_cumulative=np.cumsum(y_observed_normed)

# Step 2 - try a few distributions
DISTRIBUTIONS = [st.rayleigh, st.norm, st.uniform, st.cauchy]
DISTRIBUTIONS = [ st.norm]
best_error=np.inf
for distribution in DISTRIBUTIONS:
    params=distribution.fit(data_repeat)
    y_theory_cum=distribution.cdf(x_observed, *params)
    mse=np.mean(np.power(y_observed_cumulative-y_theory_cum,2))
    if mse<best_error:
        best_error=mse
        best_dist=distribution
        best_params=params
        best_cum_dist=y_theory_cum

# Step 3 - plot the observed vs fitted cumulative distribution
plt.figure(figsize=(6,8))
plt.suptitle('Best fitted distribution \n'+best_dist.__class__.__name__)
plt.subplot(2,1,1)
plt.plot(x_observed, y_observed_cumulative, label='observed')
plt.plot(x_observed, best_cum_dist, label='fitted')
plt.legend()
plt.title('cumulative density functions')

# Step 4 - plot the observed vs fitted cumulative distribution
plt.subplot(2,1,2)
plt.hist(x_observed, bins=20, normed=True)
pdf=best_dist.pdf(x_observed,*best_params)
plt.plot(x_observed,pdf)
plt.title('probability density functions')
plt.subplots_adjust(top=0.85)
plt.show()
