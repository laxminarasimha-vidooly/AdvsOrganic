# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 18:27:30 2019

@author: chiru
"""


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

os.chdir("E:/Laxmi_Rnd/My Laptop/AD_vs_organic_train_updated")
df=pd.read_excel("train_data_3_v2.xlsx")
df=shuffle(df)
df.head()
df.info()

def derive_columns(df):
    
    df['views_c']=df['views']/10000
    df['eng_c']=df['engagement']/500
    df['log_of_v/e']=np.log(df['views']/df['engagement'])
    df['eng_per']=(df['engagement']/df['views'])*100
#    df['published_date']=df['published_date'].map(lambda x:x.split('T')[0])
#    df['published_date']=pd.to_datetime(df['published_date'])
#    d0=date(2019,6,6)
#    d0=pd.to_datetime(d0)
#    d1=df['published_date']
#    delta=d0-d1
#    df['days']=delta.astype('str').map(lambda x:x.split(' ')[0]).astype('int')
#    df['views/days']=df['views']/df['days']
#    df['eng/days']=df['engagement']/df['days']
#    df['ratio']=df['views/days']/df['eng/days']    
    return df

df=derive_columns(df)

#########################################################################
## DATA Visualization
#
#
#########  Ratio of views and engagemnet with respect to days
#
#plt.figure(figsize=(10,10))
#sns.scatterplot(x='ratio',y='AD_per',data=df)
#plt.xlim(0,2000)
#################   Log value
#
#plt.figure(figsize=(10,10))
#sns.scatterplot(x='Log_v/e',y='AD_per',data=df)
#
##########################################################################

df.info()
df_train=df[['eng_per','views_c','eng_c','ADVERTISING']]
df_train.head()

df_train.head()
y=df_train.pop('ADVERTISING')

x_train,x_test,y_train,y_test=train_test_split(df_train,y,test_size=0.3,random_state=100)
x_train.head()
x_test.shape

folds=KFold(n_splits=2,shuffle=True,random_state=100)
hyper_param=[{'C':[1,10,100]}]
model=svm.SVR(kernel='linear', tol=0.01,epsilon=0.1)
model_3_cv=GridSearchCV(estimator=model,cv=folds,param_grid=hyper_param,scoring='neg_mean_squared_error',return_train_score=True)


model_3_cv.fit(x_train,y_train)
model_3_cv.best_params_

model_3=svm.SVR(kernel='linear',C=model_3_cv.best_params_['C'],gamma='auto',tol=0.01)

model_3.get_params

model_3.fit(x_train,y_train)

y_pred_3=model_3.predict(x_test)

c=[i for i in range(len(y_test.index))]
plt.figure(figsize=(18,10))
plt.plot(c,y_test)

plt.plot(c,y_pred_3)

from sklearn.metrics import mean_squared_error,r2_score
mse_2=mean_squared_error(y_test,y_pred_3)
print(r2_score(y_test,y_pred_3))
print(mse_2)

from sklearn.externals import joblib
joblib.dump(model_3,'model_3.pkl')



#x_test_1=df.loc[y_test.index]
#x_test_1['predict_ad']=y_pred_3
#x_test_1=x_test_1.reset_index()
#x_test_1.to_csv("test_ka_train_model_3.csv")
#len(y_test.index)
