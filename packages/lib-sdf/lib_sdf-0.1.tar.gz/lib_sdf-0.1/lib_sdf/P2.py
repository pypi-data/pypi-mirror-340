#2 Data Frames and Basic Data Pre-processing

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ds = pd.read_csv('P2.csv')
print("Data Head:\n",ds.head())
print("Data Describe:\n",ds.describe())

X = ds.iloc[:,:-1].values
Y = ds.iloc[:,3].values
print("\nInput:",X)
print("\nOutput:",Y)

# HANDLING MISSING VALUES
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(missing_values = np.nan,strategy = "mean")
imputer = imputer.fit(X[:,1:3])
X[:,1:3] = imputer.fit_transform(X[:,1:3])
print("\nNew Input with mean value for Nan:",X)

# OUTLIERS
import sklearn
from sklearn.datasets import load_diabetes
import pandas as pd
import matplotlib.pyplot as plt

db = load_diabetes()

column_name = db.feature_names
df_db = pd.DataFrame(db.data)
df_db.columns = column_name
df_db.head()

import seaborn as sns

sns.boxplot(df_db['bmi'])

import numpy as np

print(np.where(df_db['bmi']>0.12))

# SORTING
print(df_db)
sorted = df_db.sort_values(by = ["age"])
print(sorted)

# FILTERING ROWS
a = df_db.query('age>0')
print(a)
# FILTERING COLUMNS
b = df_db.filter(['age','bp'])
print(b)
# GROUPING DATA
g = df_db.groupby('age')
g.first()

print("DONE")
