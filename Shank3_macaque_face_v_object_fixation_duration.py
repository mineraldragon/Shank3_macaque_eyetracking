# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 12:36:27 2017


@author: Rogier
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#matplotlib.use('TkAgg')
#import matplotlib.pyplot as plt
#import h5py
import os.path
import time
from scipy import stats
from scipy.interpolate import UnivariateSpline
import math


df_meanpupil1=pd.DataFrame()

os.chdir('C:\\Users\\Rogier\\Documents\\Python Scripts\\')
teller=0
elapsed=[]
IDS=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5']
IDS=['C1']
plt.close('all')

df_fix_duration1=pd.DataFrame(np.nan,index=[0],columns=IDS)

fig = plt.figure()

for animal_ID in IDS:
    
    print(animal_ID)
    startpoint = time.time()
    teller=teller+1

    dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Face_v_Object\\'
    str1= dir1 + animal_ID + '.tsv'
    df = pd.read_csv(str1,sep='\t') #read tsv into dataframe

    df['total1']=np.nan
    df['AOIfHit']=np.nan
    df['AOIoHit']=np.nan

    COLUMNS=df.shape[1] #0, 1 columns (19170)
    ROWS=df.shape[0]   
    for x in range(0, COLUMNS):
        if 'AOI[f]Hit' in df.columns[x]:
#            print('yes')
#            fig, axes = plt.subplots(nrows=2, ncols=2)
#            df[df.columns[x]].plot(ax=axes[0,0],kind='line')
            df['face'] = df.fillna(0)[df.columns[x]] + df.fillna(0)['total1']
            df.loc[df[df.columns[x]].isnull() & df['total1'].isnull(),'face']=np.nan
            df['total1']=df['face']
 
    df['total1']=np.nan
    for x in range(0, COLUMNS):
        if 'AOI[o]Hit' in df.columns[x]:
            df['object'] = df.fillna(0)[df.columns[x]] + df.fillna(0)['total1']
            df.loc[df[df.columns[x]].isnull() & df['total1'].isnull(),'object']=np.nan
            df['total1']=df['object']
         
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
#    
#    
    df['face'] = df['face'].fillna(0)
    df['face'] = df['face'].replace(0,False)
    df['face'] = df['face'].replace(1,True)
    df['face'] = df.face.astype(int)
    
    df['object'] = df['object'].fillna(0)
    df['object'] = df['object'].replace(0,False)
    df['object'] = df['object'].replace(1,True)
    df['object'] = df.object.astype(int)
    
    df_face=df[df['face']==1]
    df_object=df[df['object']==1]


#
#    df_face=df[df['face']==1]
#    df_temp1=pd.DataFrame(data=df_face['FixationIndex'])
#    df_temp1['fix']=df_face['FixationIndex'].fillna(0)
#    df_temp1['fix'] = df_temp1['fix'].replace(-1, 0)
#    df_temp1['C'] = df_temp1['fix'].diff()        
#    
#    df_temp2=pd.DataFrame() 
#    df_temp2['start']=df_temp1['C'].loc[df_temp1['C']>0].index
#    df_temp2['stop']=df_temp1['C'].loc[df_temp1['C']<0].index        
#    df_temp2['duration']=df_temp2['stop']-df_temp2['start']
#    v=df_temp2['duration'].mean(axis=0)
#    df_fix_duration1[animal_ID]=v 
#
#
#    
#    #looking time by emotional content
#    bool1 = (df['object']) & (df['stim_on'])
#    a=float(sum(bool1))
#    bool2 = (df['object']) & (df['eyes_on_screen'])
#    b=float(sum(bool2))
#    res = {'object':b/a}
#    
#    bool1 = (df['face']) & (df['stim_on'])
#    a=float(sum(bool1))
#    bool2 = (df['face']) & (df['eyes_on_screen'])
#    b=float(sum(bool2))
#    res['face']=b/a
#    res['meanpupil']=df['meanpupil'].mean()
#     
#    df_fract = pd.DataFrame(data=res,index=[0])
#       
#    df_temp = pd.DataFrame(data=df['face']) 
#    df_temp['face'] = df_temp['face'].replace(False, 0)
#    df_temp['face'] = df_temp['face'].replace(True, 1)
#    df_temp['face'] = df_temp['face'].fillna(0)
#    df_temp['face'] = df_temp['face'].astype('int')
#    df_temp['D'] = df_temp['face'].diff()
#    df_temp1=pd.DataFrame(data=df_temp.loc[df_temp['D'] == 1].index.tolist(),columns=['start'])
#    df_temp1['stop']=df_temp.loc[df_temp['D'] == -1].index.tolist()
#    ROWS=df_temp1.shape[0]
#    
#    df_cum = pd.DataFrame(np.nan, index=[0], columns=['A'])
#    df_temp3 = pd.DataFrame(np.nan, index=[0], columns=['trace'])
#    for x in range(0, ROWS):
#        a = df[df_temp1.loc[x]['start']:df_temp1.loc[x]['stop']]['meanpupil']
#        a=a.reset_index(drop=True)
#        df_cum=pd.concat([df_cum, a], ignore_index=True, axis=1)
#       
#    df_pupresult = pd.DataFrame(data=df_cum.mean(axis=1),columns=['face'])
#    df_pupresult['face'] = df_pupresult['face'] - df_pupresult['face'].iloc[0]
#    df_pupresult['face'] = df_pupresult['face']
#    
#    
#    ax = fig.add_subplot(4, 4, teller)
#    df_pupresult.plot(ax=plt.gca(),title=animal_ID, xlim=[0, 50], legend='false')
#    ax.legend_.remove()
#  
#    
#    
#    #pupil reflex
#    
#    df_temp=pd.DataFrame(data=df['stim_on']) 
#    df_temp['stim_on']=df['stim_on'].fillna(0)
#    df_temp['stim_on'] = df_temp['stim_on'].replace(-1, 0)
#    df_temp['C'] = df_temp['stim_on'].diff()
#    #df_temp['C'].hist()
#    df_temp1=pd.DataFrame(data=df_temp.loc[df_temp['C'] == 1].index.tolist(),columns=['start'])
#    #now get pupil for every start
#    df_cum1 = pd.DataFrame(np.nan, index=[0], columns=['A'])#empty dataframe
#    L=df_temp1.shape[0]#nrows
#    for x in range(0, L):
#            #print(df_temp1.loc[x]['start'])
#            #selecting row 1, column 'A'
##df_test['A'].iloc[0]
##df_test.iloc[0]
#        a = df.loc[df_temp1.loc[x]['start']:df_temp1.loc[x]['start']+400,'meanpupil']
#        a=a.reset_index(drop=True)
#        df_cum1=pd.concat([df_cum1, a], ignore_index=True, axis=1)#add column to df_cum1 for each start found      
#        
#    df_cum1['sum_num'] = df_cum1.mean(axis=1)   #mean pupil response 
#            
#    df_meanpupil1[animal_ID]=df_cum1['sum_num'] #put into meanpupil
#
#            
#            
#    
#    
#    
#    
#    
#    
#    
#    
#    
#    
#    #save to hdf5
#    hdf_name=dir1+animal_ID+'.h5'
#    if os.path.isfile(hdf_name):
#        os.remove(hdf_name)
#    
#    hdf = pd.HDFStore(hdf_name)
#    
#    df.to_hdf(hdf_name, 'df', table=True, mode='a',complevel=9)
#    df_fract.to_hdf(hdf_name, 'df_fract', table=True, mode='a',complevel=9)
#    hdf.close()
#    
#    
#    
#
#q=df_meanpupil1.iloc[1:]
#q_minzero=q;
#q_minzero=q_minzero-q_minzero.iloc[1]
#
##minimum
#Dm=q.min()
#Dm_idx=q.idxmin()
#D0=q.iloc[0]
##constriction amplitude
#CAmpl=(D0-Dm)/D0
#CAmpl_rl=D0-Dm
#qx=range(400)
#
##start_constriction=pd.Series()
#
#mn_idx=[]
#
#count=0
#for animal_ID in IDS:
#    y=q[[animal_ID]]
#    
#    s=UnivariateSpline(qx, y, s=0.1, k=4)
#    ss=s(qx);
#    count=count+1
#    fnd=0
#    cnt=0
#    while fnd==0:
#        cnt=cnt+1
#        tmp=y.iloc[cnt] < (D0[animal_ID]-0.05*CAmpl_rl[animal_ID])
#        tmp=ss[cnt] < (ss[0]-0.15*CAmpl_rl[animal_ID])
#        
#        #if(tmp[0]==True):
#        if(tmp):
#            fnd=1
#            mn_idx.append(cnt)
#            
# 
#start_constriction = pd.Series(mn_idx)
#print(start_constriction)
#
#start_constriction=start_constriction.astype(float)*(1000/125)
#
#plt.figure()
#m1=start_constriction.loc[0:5].mean()
#m2=start_constriction.loc[6:10].mean()
#sem1=stats.sem(start_constriction.loc[0:5],axis=0)
#sem2=stats.sem(start_constriction.loc[6:10],axis=0)
#plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
#plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
#plt.xticks([1, 2],['Control','Mutant'])
##plt.ylim(-0.1, 0.1)
#plt.xlim(0.5,2.5)
#plt.ylabel('latency (ms)')
#
#h, p=stats.ranksums(start_constriction.loc[0:5] , start_constriction.loc[6:10] )
#print(h, p)
#    
#plt.figure()
#m1=CAmpl[['C1','C2','C3','C4','C5','C6']].mean()
#m2=CAmpl[['M1','M2','M3','M4','M5']].mean()
#sem1=stats.sem(CAmpl[['C1','C2','C3','C4','C5','C6']],axis=0)
#sem2=stats.sem(CAmpl[['M1','M2','M3','M4','M5']],axis=0)
#plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
#plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
#plt.xticks([1, 2],['Control','Mutant'])
#plt.xlim(0.5,2.5)
#
#h, p=stats.ranksums(CAmpl[['C1','C2','C3','C4','C5','C6']] , CAmpl[['M1','M2','M3','M4','M5']] )
#print(h, p)
#
#
#constriction_time=[]
#for i in range(0,10):
#    constriction_time.append(Dm_idx[i].astype(float)*(1000/125)-start_constriction[i])
#
#cons_time_series=pd.Series(constriction_time)
#plt.figure()
#m1=cons_time_series.loc[0:5].mean()
#m2=cons_time_series.loc[6:10].mean()
#sem1=stats.sem(cons_time_series.loc[0:5],axis=0)
#sem2=stats.sem(cons_time_series.loc[6:10],axis=0)
#plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
#plt.xticks([1, 2],['Control','Mutant'])
#plt.xlim(0.5,2.5)
#
#
#ctrl=q[['C1','C2','C3','C4','C5','C6']]
#mut=q[['M1','M2','M3','M4','M5']]
#
#plt.figure()
#ax1_cs=q[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(kind='line')
#qx=range(400)
#qy=q[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
#qy_sem=q[['C1','C2','C3','C4','C5','C6']].std(axis=1)
#for j in range(1,400):
#    qy_sem[j]=qy_sem[j]/math.sqrt(6)
#plt.errorbar(qx,qy,qy_sem)
#ax2_cs=q[['M1','M2','M3','M4','M5']].mean(axis=1).plot(kind='line')
#qy=q[['M1','M2','M3','M4','M5']].mean(axis=1)
#qy_sem=q[['M1','M2','M3','M4','M5']].std(axis=1)
#for j in range(1,400):
#    qy_sem[j]=qy_sem[j]/math.sqrt(5)
#plt.errorbar(qx,qy,qy_sem)
#plt.legend(['WT','Shank3'])
#plt.suptitle("Luminance pupil response, mean",fontsize=18)
#plt.tight_layout(rect=[0, 0.1, 1, 0.95])
#
#for timestep in range(0,400):
#    #q[['C1','C2','C3','C4','C5','C6']].iloc[timestep]
#    h, p=stats.ttest_ind(q[['C1','C2','C3','C4','C5','C6']].iloc[timestep].dropna() , q[['M1','M2','M3','M4','M5']].iloc[timestep].dropna() )
#    print(timestep, p)
#    if(p<0.05):
#        plt.plot(timestep,0,'ro')
#
#
#
#
#
#
#
#ctrl=q_minzero[['C1','C2','C3','C4','C5','C6']]
#mut=q_minzero[['M1','M2','M3','M4','M5']]
#
#plt.figure()
#
#ax1_cs=q_minzero[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(kind='line',color='b')
#qx=range(400)
#qy=q_minzero[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
#qy_sem=q_minzero[['C1','C2','C3','C4','C5','C6']].std(axis=1)
#for j in range(1,400):
#    qy_sem[j]=qy_sem[j]/math.sqrt(6)
#plt.errorbar(qx,qy,qy_sem,ecolor='b')
#
#ax2_cs=q_minzero[['M1','M2','M3','M4','M5']].mean(axis=1).plot(kind='line',color='g')
#qy=q_minzero[['M1','M2','M3','M4','M5']].mean(axis=1)
#qy_sem=q_minzero[['M1','M2','M3','M4','M5']].std(axis=1)
#for j in range(1,400):
#    qy_sem[j]=qy_sem[j]/math.sqrt(5)
#plt.errorbar(qx,qy,qy_sem,ecolor='g')
#
#plt.legend(['WT','Shank3'])
#plt.suptitle("Luminance pupil response, mean",fontsize=18)
#plt.tight_layout(rect=[0, 0.1, 1, 0.95])
#plt.xticks([0, 125, 250, 375], [0, 1, 2, 3])
#plt.xlabel('time after stim onset (s)')