#Importing libraries
import requests,json
import pprint
import pandas as pd
import numpy as np
import random
from datetime import date
from datetime import timedelta
import operator 
import isodate
import os

os.chdir("ad_vs_organic_test_updated")

# build class function
class get_ch_video_ids:
    
    # functio to get new api key
    def get_new_key(self,api_key):
        self.api_key=api_key
        print('inside get_new_key func',self.api_key)
        self.exceed_key.append(self.api_key)
        self.api_key_list.remove(self.api_key)
        #print(api_key_list)
        if(len(self.api_key_list)):
            self.api_key=random.choice(self.api_key_list)
            return self.api_key
        else:
            print("key finished")
            return None
#function to get and check status code of url for fetching videos ids
    def get_url(self,token,chid,start_date,end_date):
        
        
        print("inside get_url function api_key->",self.api_key)
        print('inside get_url function token received ',token)
        url="https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={4}&publishedAfter={1}T00:00:00Z&publishedBefore={2}T00:00:00Z&type=video&maxResults=50&order=viewCount&key={0}&pageToken={3}".format(self.api_key,start_date,end_date,token,chid)
        print("url_1",url)
        r=requests.get(url)
        while(r.status_code!=200):
            print("inside while loop",r.status_code)
            print("get new api key")
            new_key=self.get_new_key(self.api_key)
            if new_key:
                print("new key is : ",new_key)
                self.api_key=new_key
                url="https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={4}&publishedAfter={1}T00:00:00Z&publishedBefore={2}T00:00:00Z&type=video&maxResults=50&order=viewCount&key={0}&pageToken={3}".format(self.api_key,start_date,end_date,token,chid)
                print("next url",url)
                r=requests.get(url)
            else:
                print("key finished -> get_url func")
                break
            
        else:
            print("got status code success of get_url")
            
            
        return r
    
    # functin to get url and check status code of statistics of videos 
    def url_new(self,vo_id):
#        global api_key
        print("inside url_new func",self.api_key)
        url_1="https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails,topicDetails&maxResults=50&key={0}&id={1}".format(self.api_key,vo_id)
        print(url_1)
        r=requests.get(url_1)
        
        while(r.status_code!=200):
            print("inside while loop",r.status_code)
            print("get new api key")
            new_key=self.get_new_key(self.api_key)
            print("new key is : ",new_key)
            if new_key:
                api_key=new_key
                url_1="https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails,topicDetails&maxResults=50&key={0}&id={1}".format(api_key,vo_id)
                print("next url",url_1)
                r=requests.get(url_1)
            else:
                print(" key finished -> url_new func")
                break
        else:
            print("got status code success of url_new")
    
    
        return r
    
    
    def video_stats(self,r_dict_1):
        print('getting videos ')
#        global index
        
        for i in range(len(r_dict_1['items'])):
            self.df.loc[self.index,'video_id_list']=r_dict_1['items'][i].get('id','NA')
            self.df.loc[self.index,'video_title']=r_dict_1['items'][i]['snippet'].get('title','NA')
            self.df.loc[self.index,'channel_id']=r_dict_1['items'][i]['snippet'].get('channelId','NA')
            self.df.loc[self.index,'channel_title']=r_dict_1['items'][i]['snippet'].get('channelTitle','NA')
            if r_dict_1['items'][i].get('statistics'):
                self.df.loc[self.index,'views']=r_dict_1['items'][i]['statistics'].get('viewCount',0)
                self.df.loc[self.index,'likes']=r_dict_1['items'][i]['statistics'].get('likeCount',0)
                self.df.loc[self.index,'dislikes']=r_dict_1['items'][i]['statistics'].get('dislikeCount',0)
                self.df.loc[self.index,'comment']=r_dict_1['items'][i]['statistics'].get('commentCount',0)
            self.df.loc[self.index,'category']=r_dict_1['items'][i]['snippet'].get('categoryId',0)
            self.df.loc[self.index,'publilshed_date']=r_dict_1['items'][i]['snippet'].get('publishedAt','NA')
            if r_dict_1['items'][i].get('contentDetails'):
                self.df.loc[self.index,'YT_duration']=r_dict_1['items'][i]['contentDetails'].get('duration','NA')
            self.index+=1
        print("current_shape",self.df.shape)
       
        
    def __init__(self,start_date,end_date,gap_days=0):
        columns=['video_id_list','channel_id','channel_title','video_title','category','publilshed_date','YT_duration','views','likes','dislikes','comment']
        self.df=pd.DataFrame(columns=columns)
        # listing api_keys
        self.api_key_list=["keys"]
        # exhausted keys are inserted into exceed key
        self.exceed_key=[]
        self.api_key=self.api_key_list[0]   
        self.index=0      
        self.token=''
        self.s_date=[]
        self.e_date=[]
        self.start_d=start_date
        self.end_d=end_date
        self.gap_days=gap_days
        
    # function to fetch video id and pass it to stats api 
    def get_videos(self,r_dict):    
        video_id=[]
        try:
            
            for i in range((len(r_dict['items']))):
                video_id.append(r_dict['items'][i]['id']['videoId'])
            vi_ids=",".join(video_id)
            print("print video ids ",vi_ids)
            stats_dict=json.loads(self.url_new(vi_ids).text)
            self.video_stats(stats_dict)
        except:
            print(" can't fetch video id at the moment")
        
    #function to get next page token 
    def get_v(self,token,chid,start_date,end_date):
        print("in get v function")
        v_dict=json.loads(self.get_url(token,chid,start_date,end_date).text)
        print("to get first page videos")
        self.get_videos(v_dict)
        self.token=v_dict.get("nextPageToken")
        print(" got next page token",self.token)
        while self.token:
            
            v_dict=json.loads(self.get_url(self.token,chid,start_date,end_date).text)
            self.get_videos(v_dict)
            self.token=v_dict.get("nextPageToken")
            print(self.token)
        self.token=''

    
    #function to split date into split days
    def split_dat(self,start_date,end_date,split_date):
        while(end_date>start_date):
            print("condition 1 passed")
            
            if(self.gap_days==0):
                print('gap days is zero')
                self.s_date.append(start_date)
                self.e_date.append(end_date)
                break
            new_end_date=start_date+split_date
            while (new_end_date<end_date):
                #print("new end _Date",new_end_date)
                #print(start_date,"  :  ",new_end_date)
                self.s_date.append(start_date)
                self.e_date.append(new_end_date)
                start_date=new_end_date
                new_end_date=start_date+split_date
            else:
                print("in else block")
                #print(start_date,"  ",new_end_date,"  ",end_date)
                #print(start_date,"  :  ",end_date)
                self.s_date.append(start_date)
                self.e_date.append(end_date)
                start_date=end_date
                #print(start_date,":::",end_date)        
    #video id stats updation        
    def fetch_stats(self,filename):  
        print(self.end_d-self.start_d)
        split_d=timedelta(days=self.gap_days)
        
        self.split_dat(self.start_d,self.end_d,split_d)
        date_df=pd.DataFrame({'start_date':self.s_date,'end_date':self.e_date})
        print(date_df)
        ch_id=pd.read_csv(filename)
        print(ch_id)
        for x_chid in ch_id.channel_id:
            print(x_chid)
            for p_date in range(date_df.start_date.count()):
                self.get_v(self.token,x_chid,date_df.start_date[p_date],date_df.end_date[p_date])
        self.df['views']=self.df['views'].astype(int)
        self.df['likes']=self.df['likes'].astype(int)
        self.df['dislikes']=self.df['dislikes'].astype(int)
        self.df['comment']=self.df['comment'].astype(int)
        self.df['engagement']=self.df['likes']+self.df['dislikes']+self.df['comment']
        
        return self.df
    
#ch=get_ch_video_ids(date(2018,6,1),date(2019,5,31),15)
#ch.fetch_stats('ch_id.csv').to_csv('ch_id_result.csv')

            
