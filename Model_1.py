# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:13:30 2019

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

df=pd.read_excel("train_data_1.xlsx")
df=shuffle(df)
df.head()
df.info()
df.isnull().sum()
def derive_columns(df):
    
    df['views_c']=df['views']/1000
    df['eng_c']=df['engagement']/50
    df['log_of_v/e']=np.log(df['views']/df['engagement'])
    df['eng_per']=(df['engagement']/df['views'])*100
#    df['views_c_sq']=df['views_c']**2
##    df['eng_c_sq']=df['eng_c']**2
#    df['published_date']=df['published_date'].map(lambda x:x.split('T')[0])
#
#    df['published_date']=pd.to_datetime(df['published_date'])
#    
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
# DATA Visualization


#########  Ratio of views and engagemnet with respect to days
#
#plt.figure(figsize=(10,10))
#sns.scatterplot(x='ratio',y='AD_per',hue='classification',data=df)
#plt.xlim(0,2000)
#################   Log value
#
#plt.figure(figsize=(10,10))
#sns.scatterplot(x='Log_v/e',y='AD_per',hue='classification',data=df)

##########################################################################
#df.ratio.describe()
#df.ratio.quantile(.90)
#df=df.loc[(df.ratio<df.ratio.quantile(.90))]
df_train=df.loc[:,['views','eng_per','engagement','views_c','eng_c','classification']]
df_train.head()

# standardizing data
scaler=StandardScaler()
num_vars=['views','views_c','eng_c','engagement']
df_train[num_vars]=scaler.fit_transform(df_train[num_vars])

df_train.head()

y=df_train.pop('classification')
# train test split


x_train,x_test,y_train,y_test=train_test_split(df_train,y,test_size=0.3,random_state=100)

# train model
folds=KFold(n_splits=5,shuffle=True,random_state=100)
hyper_param=[{'C':[0.01,0.1,1,10,100]}]
model=svm.SVC(kernel='linear', decision_function_shape='ovo',gamma='scale', tol=0.01, probability=False)

model_1_cv=GridSearchCV(estimator=model,param_grid=hyper_param,scoring='recall',
                     cv=folds,verbose=1,return_train_score=True)

model_1_cv.fit(x_train,y_train)
result=model_1_cv.best_params_['C']
result

model_1=svm.SVC(kernel='linear', decision_function_shape='ovr',gamma='scale', tol=0.01, C=result
                    ,probability=True)
model_1.fit(x_train,y_train)
model_1.coef_
x_test.head()

y_pred=model_1.predict(x_test)
y_pred_prob=model_1.predict_proba(x_test)
metrics.confusion_matrix(y_test,y_pred)


metrics.recall_score(y_test,y_pred)

metrics.precision_score(y_test,y_pred)
model_1.score(x_train,y_train)

metrics.accuracy_score(y_test,y_pred)

ad_pred_prob=y_pred_prob[:,1]
fpr,tpr,thresholds=metrics.roc_curve(y_test,ad_pred_prob,drop_intermediate=False)
plt.plot(fpr,tpr,label='ROC curve')
print( " AUC score" , metrics.roc_auc_score(y_test,ad_pred_prob))

from sklearn.externals import joblib
joblib.dump(model_1,'model_1.pkl')

###############################################################
#  Model evaluation 

test_check=df.loc[(y_test.index)]
test_check['predict']=y_pred
plt.figure(figsize=(10,10))
sns.scatterplot(x='Log_v/e',y='AD_per',hue='predict',data=test_check)


