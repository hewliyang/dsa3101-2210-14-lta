
# Set up#

import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

#can try filtering or plot histogram to see what would be a good threshold
d = pd.read_csv("density_data.csv",names=["...1","CameraID","ImageLink","Latitude","Longitude","density1","density2","timestamp"])[1:]
d1 = d["density1"].to_numpy()
d2 = d["density2"].to_numpy()
density = pd.to_numeric(np.append(d2,d1))
density_without_zeros = density[density!=0]

"""# Functions"""

def scale(dat):
  df1 = pd.DataFrame(MinMaxScaler().fit_transform(dat.reshape(-1,1))).rename({0: 'min_max'}, axis=1)
  df2 = pd.DataFrame(StandardScaler().fit_transform(dat.reshape(-1,1))).rename({0: 'std_scale'}, axis=1)
  df3 = pd.DataFrame(RobustScaler().fit_transform(dat.reshape(-1,1))).rename({0: 'robust_scale'}, axis=1)
  return pd.DataFrame(pd.concat([pd.DataFrame(dat),df1, df2, df3], axis=1))

def scale_normalise(dat):
  df1 = pd.DataFrame(MinMaxScaler().fit_transform(dat.reshape(-1,1))).rename({0: 'min_max'}, axis=1)

  df2 = pd.DataFrame(StandardScaler().fit_transform(dat.reshape(-1,1)))
  df2 = pd.DataFrame(sklearn.preprocessing.normalize(df2, axis=0, copy=True, return_norm=False)).rename({0: 'std_scale'}, axis=1)

  df3 = pd.DataFrame(RobustScaler().fit_transform(dat.reshape(-1,1)))
  df3 = pd.DataFrame(sklearn.preprocessing.normalize(df3, axis=0, copy=True, return_norm=False)).rename({0: 'robust_scale'}, axis=1)

  return pd.DataFrame(pd.concat([pd.DataFrame(dat),df1, df2, df3], axis=1))

def hist_plot(dat):
  fig, axes = plt.subplots(nrows=2,ncols=2,figsize=(15, 15))
  dat["min_max"].plot(ax = axes[0,0], subplots=True,kind="hist") 
  axes[0,0].set_title("min max")
  dat["std_scale"].plot(ax = axes[0,1], subplots=True,kind="hist") 
  axes[0,1].set_title("std scale")
  dat["robust_scale"].plot(ax = axes[1,0], subplots=True,kind="hist")
  axes[1,0].set_title("robust scale")

"""# Outlier detection

"""

#to remove outliers
con = 0.001
iso = IsolationForest(contamination=con)
yhat = iso.fit_predict(density.reshape(-1,1))
density_nonoutliers = density[yhat != -1]
density_outliers = density[yhat == -1]
num_outliers = np.size(density_outliers)

iso2 = IsolationForest(contamination=con)
yhat2 = iso2.fit_predict(density_without_zeros.reshape(-1,1))
test = density_without_zeros[yhat2 != -1]

"""# Density with zeros"""

#scaling data with outliers using minmax, standard, robust 
with_outliers = scale(density)
normalise_all = scale_normalise(density)

#scaling data without outliers using minmax, standard, robust 
without_outliers = scale(density_nonoutliers)
normalise_without_outliers = scale_normalise(density_nonoutliers)

"""# Density without zeros"""

#scaling data with outliers using minmax, standard, robust 
scaled_no_zeros = scale(density_without_zeros)
scaled_normalised_no_zeros = scale_normalise(density_without_zeros)

#scaling data without outliers using minmax, standard, robust 
density_without_zerosAndoutliers = scale(test)
density_without_zerosAndoutliers_normalised = scale_normalise(test)

"""# Plots"""
## only uncomment when you want to see figures else it will be messy
##hist_plot(with_outliers)
##
##hist_plot(normalise_all)
##
##hist_plot(without_outliers)
##
##hist_plot(normalise_without_outliers)
##
##hist_plot(scaled_no_zeros)
##
##hist_plot(scaled_normalised_no_zeros)
##
##hist_plot(density_without_zerosAndoutliers)
##
##hist_plot(density_without_zerosAndoutliers_normalised)
