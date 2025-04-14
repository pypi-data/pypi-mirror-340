#6.Regression and Types
# INTERNET REQUIRED

import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score

housing = fetch_california_housing()
housing_df = pd.DataFrame(housing.data,columns=housing.feature_names)
print(housing_df)
housing_df['PRICE'] = housing.target

X = housing_df[['AveRooms']]
Y = housing_df['PRICE']
X_train, X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

model = LinearRegression()

model.fit(X_train,Y_train)

Y_pred = model.predict(X_test)

mse = mean_squared_error(Y_test,Y_pred)
r2 = r2_score(Y_test,Y_pred)

print("Mean Squared Error:",mse)
print("R-squared:",r2)
print("Intercept:",model.intercept_)
print("Coefficient:",model.coef_)

X = housing_df.drop('PRICE',axis=1)
Y = housing_df['PRICE']
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

model = LinearRegression()
model.fit(X_train,Y_train)
Y_pred = model.predict(X_test)
mse = mean_squared_error(Y_test,Y_pred)
r2 = r2_score(Y_test,Y_pred)

print("MSE:",mse)
print("R-sqaured:",r2)
print("Intercept:",model.intercept_)
print("Coefficients:",model.coef_)
