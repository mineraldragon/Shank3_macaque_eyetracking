
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

teller=-1
elapsed=[]
#IDS=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5']
IDS=['C1']

#df_fractwatched_1=pd.DataFrame(np.nan,index=IDS,columns=['submissive', 'neutral', 'threat'])
#df_fractwatched_2=pd.DataFrame(np.nan,index=IDS,columns=['submissive', 'neutral', 'threat'])
#df_fractwatched_3=pd.DataFrame(np.nan,index=IDS,columns=['submissive', 'neutral', 'threat'])

df_fractwatched_1=pd.DataFrame()
df_fractwatched_2=pd.DataFrame()
df_fractwatched_3=pd.DataFrame()

df_pupresult_1_ag=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_pupresult_1_ne=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_pupresult_1_su=pd.DataFrame(np.nan,index=[0],columns=IDS)

df_pupresult_2_ag=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_pupresult_2_ne=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_pupresult_2_su=pd.DataFrame(np.nan,index=[0],columns=IDS)

df_pupresult_3_ag=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_pupresult_3_ne=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_pupresult_3_su=pd.DataFrame(np.nan,index=[0],columns=IDS)

df_cumsum1=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_cumsum2=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_cumsum3=pd.DataFrame(np.nan,index=[0],columns=IDS)

df_meanpup1=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_meanpup2=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_meanpup3=pd.DataFrame(np.nan,index=[0],columns=IDS)

df_stim_on1=pd.DataFrame()
df_stim_on2=pd.DataFrame()
df_stim_on3=pd.DataFrame()
df_stim_on4=pd.DataFrame()

df_meanpupil1=pd.DataFrame(np.nan,index=range(0,400),columns=IDS)
df_meanpupil2=pd.DataFrame(np.nan,index=range(0,400),columns=IDS)
df_meanpupil3=pd.DataFrame(np.nan,index=range(0,400),columns=IDS)
df_meanpupil4=pd.DataFrame(np.nan,index=range(0,400),columns=IDS)
df_meanpupil5=pd.DataFrame(np.nan,index=range(0,400),columns=IDS)

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

    for round1 in range(1,2):        

        if(round1==0):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\firstround\\'
            str1= dir1 + animal_ID + '.h5'
        if(round1==1):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Second_round\\'
            str1= dir1 + animal_ID + '.h5'
        if(round1==2):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Mixed_order\\'
            str1= dir1 + animal_ID + '.h5'

        df_fract=pd.read_hdf(str1,'df_fract')
        df_cum1=pd.read_hdf(str1,'df_cum1')
        df_pupresult=pd.read_hdf(str1,'df_pupresult')
        df_media=pd.read_hdf(str1,'df_media')
        df_all=pd.read_hdf(str1,'df')
        
        
        keepers = pd.read_csv('E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Lipsmacking_second_round\\Book1.csv',sep=',')
        #0=good
        
        if(round1==0):
            df_fractwatched_1[animal_ID]=[df_fract['submissive'].iloc[0], df_fract['neutral'].iloc[0], df_fract['threat'].iloc[0]]
            df_pupresult_1_ag[animal_ID]=df_pupresult['ag']    
            df_pupresult_1_ne[animal_ID]=df_pupresult['ne']  
            df_pupresult_1_su[animal_ID]=df_pupresult['su']    
            df_cumsum1[animal_ID]=df_cum1['sum_num']
            df_meanpup1[animal_ID]=df_fract['meanpupil']


        if(round1==1):
            df_fractwatched_2[animal_ID]=[df_fract['submissive'].iloc[0], df_fract['neutral'].iloc[0], df_fract['threat'].iloc[0]]
            df_pupresult_2_ag[animal_ID]=df_pupresult['ag']    
            df_pupresult_2_ne[animal_ID]=df_pupresult['ne']  
            df_pupresult_2_su[animal_ID]=df_pupresult['su']                
            df_cumsum2[animal_ID]=df_cum1['sum_num']
            df_meanpup2[animal_ID]=df_fract['meanpupil']         
            

            
        if(round1==2):
            df_fractwatched_3[animal_ID]=[df_fract['submissive'].iloc[0], df_fract['neutral'].iloc[0], df_fract['threat'].iloc[0]]
            df_pupresult_3_ag[animal_ID]=df_pupresult['ag']    
            df_pupresult_3_ne[animal_ID]=df_pupresult['ne']  
            df_pupresult_3_su[animal_ID]=df_pupresult['su']                
            df_cumsum3[animal_ID]=df_cum1['sum_num']
            df_meanpup3[animal_ID]=df_fract['meanpupil']      


# Here we're going to plot fraction watched, per emo category, per round, per genetic status

# In[84]:

teller=0
for animal_ID in IDS:

    teller=teller+1
    print(teller)

    for round1 in range(1,2):        

        if(round1==0):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\firstround\\'
            str1= dir1 + animal_ID + '.h5'
        if(round1==1):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Second_round\\'
            str1= dir1 + animal_ID + '.h5'
        if(round1==2):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Mixed_order\\'
            str1= dir1 + animal_ID + '.h5'
        if(round1==3):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Neutral_v_threat\\'
            str1= dir1 + animal_ID + '.h5'
#        if(round1==4):
#            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Face_v_Object\\'
#            str1= dir1 + animal_ID + '.h5'
            
        df_all=pd.read_hdf(str1,'df')
        #df_all['StudioTestName'].str.upper()

#change to uppercase
        df_all['StudioTestName'] = map(lambda x: x.upper(), df_all['StudioTestName'])
        #select set 1
        df_all=df_all[df_all['StudioTestName'].str.match('SET1')]
        #remove columns with 'AOI' in them
        df_all = df_all[df_all.columns.drop(list(df_all.filter(regex='AOI')))]
        
        #replace empty cells with str 'nothing'
        df_all_sub=df_all
        df_all_sub['StudioEvent'] = df_all_sub['StudioEvent'].replace(np.nan, 'nothing', regex=True)
        #only keep movistart points
        df_all_sub=df_all_sub[df_all_sub['StudioEvent'].str.match('MovieStart')]   
        df_all_sub['indices']=df_all_sub.index
        
        keepers=keepers[:-1]
        df_all_sub=df_all_sub.reset_index(drop=True)
        df_all_sub['keepers']=keepers   
        df_all_sub1=df_all_sub[df_all_sub['keepers'] == 0] 
        df_all_sub2=df_all_sub[df_all_sub['keepers'] == 1] 
        
        L=df_all_sub1.shape[0]
        
        df_pupil1 = pd.DataFrame()#empty dataframe
        for i in range(0,L):
            tmp=df_all_sub1.iloc[i]['indices']
            a=df_all.loc[tmp:(tmp+(3*125)),['meanpupil']]
            a=a.reset_index(drop=True)
            df_pupil1=pd.concat([df_pupil1,a], ignore_index=True,axis=1)  
            #df_cum1=pd.concat([df_cum1, a], ignore_index=True, axis=1)#add column to df_cum1 for each start found      


        L=df_all_sub2.shape[0]
        
        df_pupil2 = pd.DataFrame()#empty dataframe
        for i in range(0,L):
            tmp=df_all_sub2.iloc[i]['indices']
            a=df_all.loc[tmp:(tmp+(3*125)),['meanpupil']]
            a=a.reset_index(drop=True)
            df_pupil2=pd.concat([df_pupil2,a], ignore_index=True,axis=1)  
            #df_cum1=pd.concat([df_cum1, a], ignore_index=True, axis=1)#add column to df_cum1 for each start found      
    
        
df_pupil1['avg1'] = df_pupil1.mean(axis=1)
df_pupil1['avg2'] = df_pupil2.mean(axis=1)
df_pupil1['avg1'].plot(legend=True)
df_pupil1['avg2'].plot(legend=True)
plt.show()

