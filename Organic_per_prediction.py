#Importing libraries#
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
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.externals import joblib

#Importing training data and preparing data#
df=pd.read_excel("train_data_3_v2.xlsx")
df=shuffle(df)
def derive_columns(df):
    
    df['views_c']=df['views']/10000
    df['eng_c']=df['engagement']/500
    df['log_of_v/e']=np.log(df['views']/df['engagement'])
    df['eng_per']=(df['engagement']/df['views'])*100
    return df

df=derive_columns(df)
df_train=df[['eng_per','views_c','eng_c','ADVERTISING']]
y=df_train.pop('ADVERTISING')

#Train/test split#
x_train,x_test,y_train,y_test=train_test_split(df_train,y,test_size=0.3,random_state=100)

#Building model#
folds=KFold(n_splits=2,shuffle=True,random_state=100)
hyper_param=[{'C':[1,10,100]}]
model=svm.SVR(kernel='linear', tol=0.01,epsilon=0.1)
model_3_cv=GridSearchCV(estimator=model,cv=folds,param_grid=hyper_param,scoring='neg_mean_squared_error',return_train_score=True)
model_3_cv.fit(x_train,y_train)
model_3_cv.best_params_
model_3=svm.SVR(kernel='linear',C=model_3_cv.best_params_['C'],gamma='auto',tol=0.01)
model_3.get_params
model_3.fit(x_train,y_train)

#Prediction on test data#
y_pred_3=model_3.predict(x_test)
c=[i for i in range(len(y_test.index))]
plt.figure(figsize=(18,10))
plt.plot(c,y_test)
plt.plot(c,y_pred_3)

#Calculating error metrics#
mse_2=mean_squared_error(y_test,y_pred_3)
print(r2_score(y_test,y_pred_3))
print(mse_2)

#Exporting models
joblib.dump(model_3,'model_3.pkl')
