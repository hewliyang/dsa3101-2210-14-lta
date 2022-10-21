import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn import preprocessing

#applying min max and standard scaler to the density values

d = pd.read_csv("density_data.csv",
                names=["...1","CameraID","ImageLink","Latitude","Longitude",
                       "density1","density2","timestamp"])[1:]

d1 = d["density1"].to_numpy()
d2 = d["density2"].to_numpy()
density = pd.to_numeric(np.append(d2,d1))

min_max_scaler = preprocessing.MinMaxScaler()
density1 = min_max_scaler.fit_transform(density.reshape(-1,1))
df1 = pd.DataFrame(density1).rename({0: 'min_max'}, axis=1)

std_scaler = StandardScaler()
density2 = std_scaler.fit_transform(density.reshape(-1,1))
df2 = pd.DataFrame(density2).rename({0: 'std_scale'}, axis=1)

df = pd.concat([df1, df2], axis=1)

#can try filtering or plot histogram to see what would be a good threshold
