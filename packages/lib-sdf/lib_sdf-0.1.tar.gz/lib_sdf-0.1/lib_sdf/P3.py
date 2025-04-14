#3 Feature Scaling and Dummification
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import matplotlib.pyplot as plt

iris = load_iris()
data = pd.DataFrame(data=np.c_[iris['data'],iris['target']],columns=iris['feature_names']+['target'])

numerical_features = iris['feature_names']
X = data[numerical_features]
Y = data['target']

scaler_standard = StandardScaler()
X_standardized = scaler_standard.fit_transform(X)

scaler_minmax = MinMaxScaler()
X_normalized = scaler_minmax.fit_transform(X)

plt.figure(figsize=(12,4))

plt.subplot(131)
plt.scatter(X.iloc[:,0],X.iloc[:,1],c=Y,cmap='viridis')
plt.title('Original Features')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')

plt.subplot(132)
plt.scatter(X_standardized[:,0],X_standardized[:,1],c=Y,cmap='viridis')
plt.title('Standardized Features')
plt.xlabel('Feature 1(Standardized)')
plt.ylabel('Feature 2(Standardized)')

plt.subplot(133)
plt.scatter(X_normalized[:,0],X_normalized[:,1],c=Y,cmap='viridis')
plt.title('Standardized Features')
plt.xlabel('Feature 1(Normalized)')
plt.ylabel('Feature 2(Normalized)')

plt.tight_layout()
plt.show()


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data = {'Color':['Red','Blue','Green','Red','Blue'],
        'Size':['Small','Large','Medium','Medium','Small'],
        'Label':[1,0,1,0,1]
        }

df = pd.DataFrame(data)

df_encoded = pd.get_dummies(df,columns=['Color','Size'],drop_first=True)

print("Original DataFrame:")
print(df)
print("\nDataFrame after feature dummification:")
print(df_encoded)

X = df_encoded.drop('Label',axis = 1)
Y = df_encoded['Label']

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train,Y_train)

Y_pred = model.predict(X_test)

accuracy = accuracy_score(Y_test,Y_pred)
print("\nModel Accuracy:",accuracy)



