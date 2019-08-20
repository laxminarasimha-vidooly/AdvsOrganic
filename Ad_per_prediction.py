#Importing libraries#
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error,r2_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
from sklearn import svm
from datetime import date
import os

#Importing training data and preparing training data#
df=pd.read_excel("train_data_2.xlsx")
df=shuffle(df)
def derive_columns(df):
    
    df['views_c']=df['views']/10000
    df['eng_c']=df['engagement']/500
    df['log_of_v/e']=np.log(df['views']/df['engagement'])
    df['eng_per']=(df['engagement']/df['views'])*100
    return df

df=derive_columns(df)
df_train=df[['log_of_v/e','eng_per','views_c','eng_c','AD_per']]
y=df_train.pop('AD_per')

#Train/test split#
x_train,x_test,y_train,y_test=train_test_split(df_train,y,test_size=0.3,random_state=100)

#Building model#
folds=KFold(n_splits=2,shuffle=True,random_state=100)
hyper_param=[{'C':[10,100]}]
model=svm.SVR(kernel='linear', tol=0.01,epsilon=0.1)
model_2_cv=GridSearchCV(estimator=model,cv=folds,param_grid=hyper_param,scoring='neg_mean_squared_error',return_train_score=True)
model_2_cv.fit(x_train,y_train)
model_2_cv.best_params_['C']
model_2=svm.SVR(kernel='linear',C=10,gamma='auto',tol=0.01)
model_2.fit(x_train,y_train)

#Prediction on test data#
y_pred_2=model_2.predict(x_test)
c=[i for i in range(len(y_test.index))]
plt.figure(figsize=(15,10))
plt.plot(c,y_test)
plt.plot(c,y_pred_2)

#Calculating error metrics#
mse_2=mean_squared_error(y_test,y_pred_2)
print(r2_score(y_test,y_pred_2))
print(mse_2)

#Exporting model#
joblib.dump(model_2,'model_2.pkl')
