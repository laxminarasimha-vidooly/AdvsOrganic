# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 13:13:34 2019

@author: chiru
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:11:54 2019

@author: chiru
"""

import os
os.chdir("E:/Laxmi_Rnd/My Laptop/ad_vs_organic_test_updated")
import datetime
from flask import Flask,request,redirect,url_for,send_from_directory
from datetime import date
from flask_csv import send_csv
from werkzeug.utils import secure_filename
import flask
import test_model
from flask_mail import Mail,Message


UPLOAD_FOLDER="E:/Laxmi_Rnd/My Laptop/ad_vs_organic_test_updated"

app=Flask(__name__)
mail=Mail(app)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='chiranshu@vidooly.com'
app.config['MAIL_PASSWORD']='bhatia95'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

@app.route('/video_id_AD prediction',methods=['POST','GET'])
def video_ad_prediction():
    print('inside video prediction')
    if request.method=='POST':
        print(request.files['file'])
        f=request.files['file']
        email=request.form['emailId']
        project=request.form['Project']
        if('@vidooly.com'in email and f and f.filename=='source.csv' and project):
            print('inside if ')
            f.save(secure_filename(f.filename))
            result_df=test_model.ad_vs_organic(f.filename)
            file=open('log_file.csv','a')
            file.write(email+','+project+','+'video_id'+','+str(date.today())+'\n')
            file.close()
            return process(result_df,email)
        else :
            return redirect(url_for('error_video'))
        
    return '''
<html><head><title>Upload new File</title>
    </head><body><h1>Upload File contating  video ID </h1>
    <h1>file name should be source.csv with header name "video_id"</h1>
    <h1> Pass only video_ids </h1>
    <form method="post" enctype="multipart/form-data">
      <p><input type="file" name="file">
      
         <input type="submit" value="Upload">
         </p>
         <br>
         "Vidooly email Id :"
         <input type="text" name="emailId"><br>
         "Project Name:"
         <input type="text" name="Project">
         <br>
    </form></h2><div style="background-color: rgb(255, 143, 0); display: none; color: white; text-align: center; position: fixed; top: 0px; left: 0px; width: 100%; height: auto; min-width: 100%; min-height: auto; max-width: 100%; font: 12px &quot;Helvetica Neue&quot;, Helvetica, Arial, Geneva, sans-serif; cursor: pointer; padding: 5px;"><span style="color: white; font: 12px &quot;Helvetica Neue&quot;, Helvetica, Arial, Geneva, sans-serif;">You have turned off the paragraph player. You can turn it on again from the options page.</span><img src="chrome-extension://gfjopfpjmkcfgjpogepmdjmcnihfpokn/img/icons/icon-close_16.png" style="width: 20px; height: auto; min-width: 20px; min-height: auto; max-width: 20px; float: right; margin-right: 10px;"></div></body></html>
'''

def process(file,email):
    
    current_time='-'.join('_'.join(str(datetime.datetime.now().replace(microsecond=0)).split(' ')).split(':'))
    file_name='Ad_prdiction'+'_'+current_time+'.csv'
    print(file_name)
    file.to_csv(file_name)  
    download_link='http://127.0.0.1:5000/download_file/'+file_name
    msg=Message('download file link',sender='chiranshu@vidooly.com',recipients=[email])
    msg.body='''click on download link
    '''+download_link
    mail.send(msg)
    
    
    
    return ' mail send & file saved'

#    resp = flask.make_response(file.to_csv())
#    resp.headers["Content-Disposition"] = "attachment; filename=AD_prediction.csv"
#    resp.headers["Content-Type"] = "text/csv"
#    return resp 


@app.route('/download_file/<path:file_name>',methods=['GET','POST'])
def download(file_name):
    print('inside download function')
    return send_from_directory(directory=UPLOAD_FOLDER,filename=file_name)



@app.route('/channel_id_AD prediction',methods=['POST','GET'])
def channel_ad_prediction():
    
    print('inside channel prediction')
    if request.method=='POST':
        f=request.files['file']
        email=request.form['emailId']
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        gap_days=request.form['gap_days']
        project=request.form['project']
        if ('@vidooly.com' in email and f and f.filename=='ch_id.csv' and start_date and end_date and project):
            print('inside if cluase')
            start_date=date(*map(int,start_date.split('-')))
            end_date=date(*map(int,end_date.split('-')))
            if gap_days:
                gap_days=int(gap_days)
            else:
                gap_days=0
            print('start_date',start_date)
            print('end_date',end_date)
            print('gap_days',gap_days)
            result_df=test_model.ad_vs_organic_channel(f.filename,start_date,end_date,gap_days)
            file=open('log_file.csv','a')
            file.write(email+','+project+','+'channel_id'+','+str(date.today())+'\n')
            file.close()
            return process(result_df,email)
        else:
            return redirect(url_for('error_channel'))
        
        
    
    return ''' <!DOCTYPE html>
<html><head><title>Upload new File</title>
    </head><body><h1>Upload File contating  channel ID </h1>
    <h1>file name should be ch_id.csv with header name "channel_id"</h1>
    <h1> Pass only channel_ids </h1>
    <form method="post" enctype="multipart/form-data">
      <p>
      <input type='date' name='start_date'> Start_date <br>
      <input type='date' name='end_date'> End_date <br>
      <input type='text' name='gap_days'> Gap_days <br>
      <input type="file" name="file">
      
         <input type="submit" value="Upload">
         </p>
         <br>
         "Vidooly email Id :"
         <input type="text" name="emailId"><br>
         "Project Name:"
         <input type='text' name='project'><br>
         
         <br>
    </form></h2><div style="background-color: rgb(255, 143, 0); display: none; color: white; text-align: center; position: fixed; top: 0px; left: 0px; width: 100%; height: auto; min-width: 100%; min-height: auto; max-width: 100%; font: 12px &quot;Helvetica Neue&quot;, Helvetica, Arial, Geneva, sans-serif; cursor: pointer; padding: 5px;"><span style="color: white; font: 12px &quot;Helvetica Neue&quot;, Helvetica, Arial, Geneva, sans-serif;">You have turned off the paragraph player. You can turn it on again from the options page.</span><img src="chrome-extension://gfjopfpjmkcfgjpogepmdjmcnihfpokn/img/icons/icon-close_16.png" style="width: 20px; height: auto; min-width: 20px; min-height: auto; max-width: 20px; float: right; margin-right: 10px;"></div></body></html>
'''

@app.route('/RnD',methods=['POST','GET'])
def main_page():
    if request.method=='POST':
        data_type=request.form['input_data_type']
        if 'channel_ID' in data_type:
            
           return redirect(url_for('channel_ad_prediction'))
        elif 'video_ID' in data_type:
            
            return redirect(url_for('video_ad_prediction'))
        print(data_type)
        
    return '''<html><head><title>Select type of input data for AD prediction</title></head>
<body> <h1>Choose type of input_data</h1>
<form method="post" enctype="multipart/form-data">
<input type='radio' name='input_data_type' value='video_ID' checked> VIDEO_IDs <br>
<input type='radio' name='input_data_type' value='channel_ID'> CHANNEL_IDs <br>
<input type='submit' value='submit'>
</form></body></html>'''
print("helo")
@app.route('/file_error')
def error_video():
    return ''' <html><head><title> Invalid Parameters </title></head>
<body>
<h1> Invalid parameters</h1><br>
<h2> File name should be source.csv with video_id as headers</h2><br>
<h2> Enter valid email id <h2>
<h2> Project Name can't be blank</h2>
</body>
  </html>'''
@app.route('/error')  
def error_channel():
    return ''' <html><head><title> Invalid paramters</title></head>
<body>
<h1> Invalid parameters </h1><br>
<h2> File name should be ch_id.csv with channel_id as headers</h2><br>
<h2> Enter valid email id </h2><br>
<h2> Enter valid start date and end date</h2>
<h2> Project Name can't be blank</h2>
</body>
</html>
'''


    

app.run() 
