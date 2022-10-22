import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.ensemble import IsolationForest

#can try filtering or plot histogram to see what would be a good threshold
d = pd.read_csv("density_data.csv",names=["...1","CameraID","ImageLink","Latitude","Longitude","density1","density2","timestamp"])[1:]
d1 = d["density1"].to_numpy()
d2 = d["density2"].to_numpy()
density = pd.to_numeric(np.append(d2,d1))

def scale(dat):
  df1 = pd.DataFrame(MinMaxScaler().fit_transform(dat.reshape(-1,1))).rename({0: 'min_max'}, axis=1)
  df2 = pd.DataFrame(StandardScaler().fit_transform(dat.reshape(-1,1))).rename({0: 'std_scale'}, axis=1)
  df3 = pd.DataFrame(RobustScaler().fit_transform(dat.reshape(-1,1))).rename({0: 'robust_scale'}, axis=1)
  df4 = pd.DataFrame(MaxAbsScaler().fit_transform(dat.reshape(-1,1))).rename({0: 'max_abs_scale'}, axis=1)
  return pd.concat([df1, df2, df3, df4], axis=1)

#to remove outliers
iso = IsolationForest(contamination=0.001)
yhat = iso.fit_predict(density.reshape(-1,1))
density_nonoutliers = density[yhat != -1]
density_outliers = density[yhat == -1]
num_outliers = np.size(density_outliers)

#scaling data with outliers using minmax, standard, robust and maxabs
with_outliers = scale(density)

#scaling data without outliers using minmax, standard, robust and maxabs
without_outliers = scale(density_nonoutliers)
