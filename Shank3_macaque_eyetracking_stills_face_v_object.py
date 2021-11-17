
# coding: utf-8

# TODO:
# luminance pupil response
# fixation duration
# 
# 
# We're first loading all the required stuff

# In[17]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.interpolate import UnivariateSpline
import time
import math
#get_ipython().magic(u'matplotlib inline')


# In[1]:

teller=-1
elapsed=[]
IDS=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5']
#IDS=['C1']

df_fractwatched_1=pd.DataFrame()
df_fractwatched_2=pd.DataFrame()
df_fractwatched_3=pd.DataFrame()

df_pupresult_1_ag=pd.DataFrame()
df_pupresult_1_ne=pd.DataFrame()
df_pupresult_1_su=pd.DataFrame()

df_pupresult_2_ag=pd.DataFrame()
df_pupresult_2_ne=pd.DataFrame()
df_pupresult_2_su=pd.DataFrame()

df_pupresult_3_ag=pd.DataFrame()
df_pupresult_3_ne=pd.DataFrame()
df_pupresult_3_su=pd.DataFrame()

df_cumsum1=pd.DataFrame()
df_cumsum2=pd.DataFrame()
df_cumsum3=pd.DataFrame()
df_meanpup1=pd.DataFrame()
df_meanpup2=pd.DataFrame()
df_meanpup3=pd.DataFrame()

df_stim_on1=pd.DataFrame()
df_stim_on2=pd.DataFrame()
df_stim_on3=pd.DataFrame()
df_stim_on4=pd.DataFrame()
df_meanpupil1=pd.DataFrame()
df_meanpupil2=pd.DataFrame()
df_meanpupil3=pd.DataFrame()
df_meanpupil4=pd.DataFrame()
df_meanpupil5=pd.DataFrame()

df_fix_duration1=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_fix_duration2=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_fix_duration3=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_fix_duration4=pd.DataFrame(np.nan,index=[0],columns=IDS)
dfs = {}


# Loading animals one by one
# df_fract =  only mean values for pupil size and fraction watched per emo cat
# df_cum1 = pupil response any time there was a face
# df_pupresult = pupil response for ag, ne and su
# df_media = fraction watched, per clip
# df_all = everything

# In[3]:

for animal_ID in IDS:
    
    startpoint = time.time()
    teller=teller+1
    print(teller)

    for round1 in range(0,1):        

        if(round1==0):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Face_v_Object\\'
            str1= dir1 + animal_ID + '.tsv'
            df = pd.read_csv(str1,sep='\t') #read tsv into dataframe
        if(round1==1):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Neutral_v_threat\\'
            str1= dir1 + animal_ID + '_Neut_v_emo.tsv'
            df = pd.read_csv(str1,sep='\t') #read tsv into dataframe
      
        #create column with pupil mean between pupil left and right        
        df['meanpupil']=df[['PupilLeft', 'PupilRight']].mean(axis=1)  
    
        #if one of them is nan, make mean nan too
        df.loc[df['PupilLeft'].isnull() & df['PupilRight'].isnull(),'meanpupil']=np.nan  
    
        #If there is a value, that means the eyes are at the screen
        df['eyes_on_screen'] = (df['GazePointX (ADCSpx)'] > 0) & (df['GazePointY (ADCSpx)'] > 0)
    
        #if there is a medianame, that means the stim is on
        df['stim_on'] = (df['MediaName'].notnull())
    
        #save only the relevant columns to csv
        str1= dir1 + animal_ID + '_df.csv'
        header = ['StudioTestName', 'MediaName','eyes_on_screen', 'meanpupil','stim_on', 'StudioEvent', 'StudioEventData','face','object']
        df.to_csv(str1, columns = header) 
    
        df=df[df['face']==1]
    
    
        #pupil reflex   
        df_temp=pd.DataFrame(data=df['stim_on']) 
        df_temp['stim_on']=df['stim_on'].fillna(0)
        df_temp['stim_on'] = df_temp['stim_on'].replace(-1, 0)
        df_temp['C'] = df_temp['stim_on'].diff()
        #df_temp['C'].hist()
        df_temp1=pd.DataFrame(data=df_temp.loc[df_temp['C'] == 1].index.tolist(),columns=['start'])
        #now get pupil for every start
        df_cum1 = pd.DataFrame(np.nan, index=[0], columns=['A'])#empty dataframe
        L=df_temp1.shape[0]#nrows
        for x in range(0, L):
            #print(df_temp1.loc[x]['start'])
            #selecting row 1, column 'A'
#df_test['A'].iloc[0]
#df_test.iloc[0]
            a = df.loc[df_temp1.loc[x]['start']:df_temp1.loc[x]['start']+400,'meanpupil']
            a=a.reset_index(drop=True)
            df_cum1=pd.concat([df_cum1, a], ignore_index=True, axis=1)#add column to df_cum1 for each start found      
        
        df_cum1['sum_num'] = df_cum1.mean(axis=1)   #mean pupil response 
            
        if(round1==0):
            df_meanpupil1[animal_ID]=df_cum1['sum_num'] #put into meanpupil
        if(round1==1):
            df_meanpupil2[animal_ID]=df_cum1['sum_num'] #put into meanpupil


        df_temp1=pd.DataFrame(data=df['FixationIndex'])
        df_temp1['fix']=df['FixationIndex'].fillna(0)
        df_temp1['fix']= df_temp1['fix'].replace(-1, 0)
        df_temp1['C']= df_temp1['fix'].diff()     
        
        df_temp2=pd.DataFrame() 
        df_temp2['start']=df_temp1['C'].loc[df_temp1['C']>0].index
        df_temp2['stop']=df_temp1['C'].loc[df_temp1['C']<0].index        
        df_temp2['duration']=df_temp2['stop']-df_temp2['start']
        v=df_temp2['duration'].mean(axis=0)
        v=v*8
        if(round1==0):
            print(v)
            df_fix_duration1[animal_ID]=v #put into meanpupil  
            print(df_fix_duration1)
            #print(df_temp2['duration'].mean(axis=0))
        if(round1==1):
            print(v)
            df_fix_duration2[animal_ID]=v #put into meanpupil   



qfx=df_fix_duration1


plt.figure()
m1=qfx[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
m2=qfx[['M1','M2','M3','M4','M5']].mean(axis=1)
sem1=stats.sem(qfx[['C1','C2','C3','C4','C5','C6']],axis=1)
sem2=stats.sem(qfx[['M1','M2','M3','M4','M5']],axis=1)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1[0], sem2[0]], fmt='o')
plt.errorbar([1, 2],[m1, m2],yerr=[sem1[0], sem2[0]], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
plt.xlim(0.5,2.5)
plt.ylabel('fix duration (ms)')           
            
h, p=stats.ranksums(qfx[['C1','C2','C3','C4','C5','C6']].T, qfx[['M1','M2','M3','M4','M5']].T )
print(h, p)





