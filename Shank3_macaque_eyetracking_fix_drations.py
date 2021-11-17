
# coding: utf-8

# TODO:
# luminance pupil response
# fixation duration
# 
# 
# We're first loading all the required stuff

# In[17]:
    
  

import pandas as pd
from pandas import ExcelWriter
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.interpolate import UnivariateSpline
import time
import math
import os.path

#get_ipython().magic(u'matplotlib inline')

#
sample_freq=125;

teller=-1
elapsed=[]
IDS=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5']
#IDS=['C1']

df_eyes1=pd.DataFrame(np.nan,index=[0],columns={'eyes'})
df_eyes2=pd.DataFrame(np.nan,index=[0],columns={'eyes'})
df_eyes3=pd.DataFrame(np.nan,index=[0],columns={'eyes'})

df_mouth1=pd.DataFrame(np.nan,index=[0],columns={'mouth'})
df_mouth2=pd.DataFrame(np.nan,index=[0],columns={'mouth'})
df_mouth3=pd.DataFrame(np.nan,index=[0],columns={'mouth'})

df_eyemouth=pd.DataFrame(np.nan,index={'eyes', 'mouth', 'em_ratio'},columns=IDS)

dfs = {}


# In[3]:

for animal_ID in IDS:
    
    tmp_eyes=[]
    tmp_mouth=[]

    startpoint = time.time()
    teller=teller+1
    print(teller)

    for round1 in range(0,3):        

        
        
        if(round1==0):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\firstround\\'
            str1= dir1 + animal_ID + '_df.csv'
            
        if(round1==1):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Mixed_order\\'  
            str1= dir1 + animal_ID + '_df.csv'
            
        if(round1==2):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Second_round\\'  
            str1= dir1 + animal_ID + '_df.csv'            
    
        
        df = pd.read_csv(str1)
        

               
        if(round1==0):
            df_eyes1=pd.DataFrame(data=df['eyes']) 
            df_eyes1['eyes']=df_eyes1['eyes'].fillna(0)
            df_eyes1['eyes'] = df_eyes1['eyes'].replace(-1, 0)
            
            tmp=df_eyes1['eyes'].value_counts()
            tmp_eyes.append(tmp[1])

            df_mouth1=pd.DataFrame(data=df['mouth']) 
            df_mouth1['mouth']=df_mouth1['mouth'].fillna(0)
            df_mouth1['mouth'] = df_mouth1['mouth'].replace(-1, 0)
            
            tmp=df_mouth1['mouth'].value_counts()
            tmp_mouth.append(tmp[1])
            
        if(round1==1):
            df_eyes2=pd.DataFrame(data=df['eyes']) 
            df_eyes2['eyes']=df_eyes2['eyes'].fillna(0)
            df_eyes2['eyes'] = df_eyes2['eyes'].replace(-1, 0)
            
            tmp=df_eyes2['eyes'].value_counts()
            tmp_eyes.append(tmp[1])
            
            df_mouth2=pd.DataFrame(data=df['mouth']) 
            df_mouth2['mouth']=df_mouth2['mouth'].fillna(0)
            df_mouth2['mouth'] = df_mouth2['mouth'].replace(-1, 0)

            tmp=df_mouth2['mouth'].value_counts()
            tmp_mouth.append(tmp[1])
            
        if(round1==2):
            df_eyes3=pd.DataFrame(data=df['eyes']) 
            df_eyes3['eyes']=df_eyes3['eyes'].fillna(0)
            df_eyes3['eyes'] = df_eyes3['eyes'].replace(-1, 0)
            
            tmp=df_eyes3['eyes'].value_counts()
            tmp_eyes.append(tmp[1])
            
            df_mouth3=pd.DataFrame(data=df['mouth']) 
            df_mouth3['mouth']=df_mouth3['mouth'].fillna(0)
            df_mouth3['mouth'] = df_mouth3['mouth'].replace(-1, 0)            
            
            tmp=df_mouth3['mouth'].value_counts()
            tmp_mouth.append(tmp[1])        

        
    df_eyemouth[ animal_ID]['eyes'] = sum(tmp_eyes)/sample_freq
    df_eyemouth[ animal_ID]['mouth'] = sum(tmp_mouth)/sample_freq
    df_eyemouth[ animal_ID]['em_ratio'] = float(sum(tmp_eyes) - sum(tmp_mouth) ) / (sum(tmp_eyes) + sum(tmp_mouth) )
    
    
    df_fixdur[animal_ID] = df[]
        
        
q=df_eyemouth.iloc[2]    
q.plot(kind='bar')            
        
        
        
writer = pd.ExcelWriter('E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\eye_mouth_ratio.xlsx')
#q.to_excel(writer,'Sheet1')


df_eyemouth=df_eyemouth.T
df_eyemouth.to_excel(writer,'Sheet1')

writer.save()
        
        
        
