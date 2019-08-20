#Importing Libraries#
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
from sklearn.externals import joblib

#Importing training data and preparing training data#
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
 
    return df
df=derive_columns(df)
df_train=df.loc[:,['views','eng_per','engagement','views_c','eng_c','classification']]
df_train.head()

# standardizing data#
scaler=StandardScaler()
num_vars=['views','views_c','eng_c','engagement']
df_train[num_vars]=scaler.fit_transform(df_train[num_vars])
y=df_train.pop('classification')

# train test split#
x_train,x_test,y_train,y_test=train_test_split(df_train,y,test_size=0.3,random_state=100)

# train model#
folds=KFold(n_splits=5,shuffle=True,random_state=100)
hyper_param=[{'C':[0.01,0.1,1,10,100]}]
model=svm.SVC(kernel='linear', decision_function_shape='ovo',gamma='scale', tol=0.01, probability=False)
model_1_cv=GridSearchCV(estimator=model,param_grid=hyper_param,scoring='recall',
                     cv=folds,verbose=1,return_train_score=True)
model_1_cv.fit(x_train,y_train)
result=model_1_cv.best_params_['C']
model_1=svm.SVC(kernel='linear', decision_function_shape='ovr',gamma='scale', tol=0.01, C=result
                    ,probability=True)
model_1.fit(x_train,y_train)
#Prediction on test data#
y_pred=model_1.predict(x_test)
y_pred_prob=model_1.predict_proba(x_test)
#building confusion matrix and calculating precision and recall#
metrics.confusion_matrix(y_test,y_pred)
metrics.recall_score(y_test,y_pred)
metrics.precision_score(y_test,y_pred)
model_1.score(x_train,y_train)
metrics.accuracy_score(y_test,y_pred)
ad_pred_prob=y_pred_prob[:,1]
fpr,tpr,thresholds=metrics.roc_curve(y_test,ad_pred_prob,drop_intermediate=False)
plt.plot(fpr,tpr,label='ROC curve')
print( " AUC score" , metrics.roc_auc_score(y_test,ad_pred_prob))
joblib.dump(model_1,'model_1.pkl')
###############################################################
#  Model evaluation#
test_check=df.loc[(y_test.index)]
test_check['predict']=y_pred
plt.figure(figsize=(10,10))
sns.scatterplot(x='Log_v/e',y='AD_per',hue='predict',data=test_check)
