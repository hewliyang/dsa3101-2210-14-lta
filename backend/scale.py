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

#scaling data with outliers using minmax, standard, robust and maxabs

min_max_scaler = MinMaxScaler()
density1 = min_max_scaler.fit_transform(density.reshape(-1,1))
df1 = pd.DataFrame(density1).rename({0: 'min_max'}, axis=1)

std_scaler = StandardScaler()
density2 = std_scaler.fit_transform(density.reshape(-1,1))
df2 = pd.DataFrame(density2).rename({0: 'std_scale'}, axis=1)

density3 = RobustScaler().fit_transform(density.reshape(-1,1))
df3 = pd.DataFrame(density3).rename({0: 'robust_scale'}, axis=1)

density4 = MaxAbsScaler().fit_transform(density.reshape(-1,1))
df4 = pd.DataFrame(density4).rename({0: 'max_abs_scale'}, axis=1)

with_outliers = pd.concat([df1, df2, df3, df4], axis=1)

#to remove outliers
iso = IsolationForest(contamination=0.001)
yhat = iso.fit_predict(density.reshape(-1,1))
density_nonoutliers = density[yhat != -1]
density_outliers = density[yhat == -1]
num_outliers = np.size(density_outliers)

#scaling data without outliers using minmax, standard, robust and maxabs

min_max_scaler = MinMaxScaler()
densityno1 = min_max_scaler.fit_transform(density_nonoutliers.reshape(-1,1))
no1 = pd.DataFrame(densityno1).rename({0: 'min_max'}, axis=1)

std_scaler = StandardScaler()
densityno2 = std_scaler.fit_transform(density_nonoutliers.reshape(-1,1))
no2 = pd.DataFrame(densityno2).rename({0: 'std_scale'}, axis=1)

densityno3 = RobustScaler().fit_transform(density_nonoutliers.reshape(-1,1))
no3 = pd.DataFrame(densityno3).rename({0: 'robust_scale'}, axis=1)

densityno4 = MaxAbsScaler().fit_transform(density_nonoutliers.reshape(-1,1))
no4 = pd.DataFrame(densityno4).rename({0: 'max_abs_scale'}, axis=1)

without_outliers = pd.concat([no1, no2, no3, no4], axis=1)
