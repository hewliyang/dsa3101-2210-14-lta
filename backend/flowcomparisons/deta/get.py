from deta import Deta  # Import Deta
import pandas as pd
from pandas import json_normalize

# Initialize with a Project Key
deta = Deta("c02vlv6g_FTeny6UiDCzQs2QX1AUZrQg6UoZRin8h")

# This how to connect to or create a database.
db = deta.Base("density_speed_records")

res = db.fetch()
all_items = res.items

# fetch until last is 'None'
while res.last:
  res = db.fetch(last=res.last)
  all_items += res.items

df=pd.json_normalize(all_items, max_level=1)
df.to_csv(r'/Users/leyaozhu/Documents/speeddata.csv')

