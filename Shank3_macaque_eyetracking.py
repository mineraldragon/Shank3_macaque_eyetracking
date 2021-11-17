
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
IDS=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5']
#IDS=['C1']

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

df_eyes1=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_eyes2=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_eyes3=pd.DataFrame(np.nan,index=[0],columns=IDS)

df_mouth1=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_mouth2=pd.DataFrame(np.nan,index=[0],columns=IDS)
df_mouth3=pd.DataFrame(np.nan,index=[0],columns=IDS)

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

    for round1 in range(0,3):        

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
        
        if(round1==0):
            df_fractwatched_1[animal_ID]=[df_fract['submissive'].iloc[0], df_fract['neutral'].iloc[0], df_fract['threat'].iloc[0]]
            df_pupresult_1_ag[animal_ID]=df_pupresult['ag']    
            df_pupresult_1_ne[animal_ID]=df_pupresult['ne']  
            df_pupresult_1_su[animal_ID]=df_pupresult['su']    
            df_cumsum1[animal_ID]=df_cum1['sum_num']
            df_meanpup1[animal_ID]=df_fract['meanpupil']
            df_eyes1[animal_ID]=df_all['eyes']            
            df_mouth1[animal_ID]=df_all['mouth'] 

        if(round1==1):
            df_fractwatched_2[animal_ID]=[df_fract['submissive'].iloc[0], df_fract['neutral'].iloc[0], df_fract['threat'].iloc[0]]
            df_pupresult_2_ag[animal_ID]=df_pupresult['ag']    
            df_pupresult_2_ne[animal_ID]=df_pupresult['ne']  
            df_pupresult_2_su[animal_ID]=df_pupresult['su']                
            df_cumsum2[animal_ID]=df_cum1['sum_num']
            df_meanpup2[animal_ID]=df_fract['meanpupil']            
            df_eyes2[animal_ID]=df_all['eyes']  
            df_mouth2[animal_ID]=df_all['mouth'] 
            
        if(round1==2):
            df_fractwatched_3[animal_ID]=[df_fract['submissive'].iloc[0], df_fract['neutral'].iloc[0], df_fract['threat'].iloc[0]]
            df_pupresult_3_ag[animal_ID]=df_pupresult['ag']    
            df_pupresult_3_ne[animal_ID]=df_pupresult['ne']  
            df_pupresult_3_su[animal_ID]=df_pupresult['su']                
            df_cumsum3[animal_ID]=df_cum1['sum_num']
            df_meanpup3[animal_ID]=df_fract['meanpupil']      
            df_eyes3[animal_ID]=df_all['eyes']  
            df_mouth3[animal_ID]=df_all['mouth'] 
            
# Here we're going to plot fraction watched, per emo category, per round, per genetic status

# In[84]:

teller=0
for animal_ID in IDS:

    teller=teller+1
    print(teller)

    for round1 in range(0,4):        

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
        #get fixations
        df_temp1=pd.DataFrame(data=df_all['FixationIndex'])
        df_temp1['fix']=df_all['FixationIndex'].fillna(0)
        df_temp1['fix'] = df_temp1['fix'].replace(-1, 0)
        df_temp1['C'] = df_temp1['fix'].diff()        
        
        df_temp2=pd.DataFrame() 
        df_temp2['start']=df_temp1['C'].loc[df_temp1['C']>0].index
        df_temp2['stop']=df_temp1['C'].loc[df_temp1['C']<0].index        
        df_temp2['duration']=df_temp2['stop']-df_temp2['start']
        v=df_temp2['duration'].mean(axis=0)
        if(round1==0):
            df_fix_duration1[animal_ID]=v #put into meanpupil  
            #print(df_temp2['duration'].mean(axis=0))
        if(round1==1):
            df_fix_duration2[animal_ID]=v #put into meanpupil   
        if(round1==2):
            df_fix_duration3[animal_ID]=v #put into meanpupil               
        if(round1==3):
            df_fix_duration4[animal_ID]=v #put into meanpupil               
            
        #plt.figure()
        #df_temp2['duration'].hist(bins=100)
        
        df_temp=pd.DataFrame(data=df_all['stim_on']) 
        df_temp['stim_on']=df_all['stim_on'].fillna(0)
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
            a = df_all.loc[df_temp1.loc[x]['start']:df_temp1.loc[x]['start']+400,'meanpupil']
            a=a.reset_index(drop=True)
            df_cum1=pd.concat([df_cum1, a], ignore_index=True, axis=1)#add column to df_cum1 for each start found      
        
        df_cum1['sum_num'] = df_cum1.mean(axis=1)   #mean pupil response 
            
        if(round1==0):
            df_meanpupil1[animal_ID]=df_cum1['sum_num'] #put into meanpupil
        if(round1==1):
            df_meanpupil2[animal_ID]=df_cum1['sum_num'] #put into meanpupil
        if(round1==2):
            df_meanpupil3[animal_ID]=df_cum1['sum_num'] #put into meanpupil
        if(round1==3):
            df_meanpupil4[animal_ID]=df_cum1['sum_num'] #put into meanpupil
       # if(round1==4):
        #    df_meanpupil5[animal_ID]=df_cum1['sum_num'] #put into meanpupil











#dfs[0]=df_meanpupil1
#dfs[1]=df_meanpupil2
#dfs[2]=df_meanpupil3
#dfs[3]=df_meanpupil4
#dfs[3]=df_meanpupil5

dfs={}
dfs[0]=df_fix_duration1
dfs[1]=df_fix_duration2
dfs[2]=df_fix_duration3
#dfs[3]=df_fix_duration4
panel = pd.Panel(dfs)
qfx=panel.mean(axis=0)
#qfx=qfx.iloc[1:]

plt.figure()
m1=qfx[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
m2=qfx[['M1','M2','M3','M4','M5']].mean(axis=1)
sem1=stats.sem(qfx[['C1','C2','C3','C4','C5','C6']],axis=1)
sem2=stats.sem(qfx[['M1','M2','M3','M4','M5']],axis=1)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1[0], sem2[0]], fmt='o')
plt.errorbar([1, 2],[m1, m2],yerr=[sem1[0], sem2[0]], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
plt.xlim(0.5,2.5)
plt.ylabel('fix duration (samples)')


dfs={}
dfs[0]=df_meanpupil1
dfs[1]=df_meanpupil2
#dfs[2]=df_meanpupil3
panel = pd.Panel(dfs)
q=panel.mean(axis=0)
q=q.iloc[1:]

q_minzero=q;
q_minzero=q_minzero-q_minzero.iloc[1]


#minimum
Dm=q.min()
Dm_idx=q.idxmin()
D0=q.iloc[0]
#constriction amplitude
CAmpl=(D0-Dm)/D0
CAmpl_rl=D0-Dm
qx=range(399)

#start_constriction=pd.Series()


#%% 

#


mn_idx=[]
p_contr_idx=[]
count=0
for animal_ID in IDS:
    y=q[[animal_ID]]
    #z=y.values
    z=y.iloc[:, 0].tolist()
    s=UnivariateSpline(qx, z, s=0.1, k=4)
    ss=s(qx);
    count=count+1
    fnd=0
    cnt=0
    s1=UnivariateSpline(qx, z, s=0.5, k=5)
    s1_2d = s1.derivative(n=2)
    a=s1_2d(qx)
    plt.figure()
    plt.plot(qx,a)
    p_contr_idx.append(np.argmax(a))
    
    while fnd==0:
        cnt=cnt+1
        tmp=y.iloc[cnt] < (D0[animal_ID]-0.05*CAmpl_rl[animal_ID])
        tmp=ss[cnt] < (ss[0]-0.15*CAmpl_rl[animal_ID])
        
        #if(tmp[0]==True):
        if(tmp):
            fnd=1
            mn_idx.append(cnt)
            

start_constriction = pd.Series(mn_idx)
start_constriction2 = pd.Series(p_contr_idx) 
print(start_constriction)
print(start_constriction2)

start_constriction=start_constriction.astype(float)*(1000/125)
start_constriction2=start_constriction2.astype(float)*(1000/125)

plt.figure()
m1=start_constriction.loc[0:5].mean()
m2=start_constriction.loc[6:10].mean()
sem1=stats.sem(start_constriction.loc[0:5],axis=0)
sem2=stats.sem(start_constriction.loc[6:10],axis=0)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
#plt.ylim(-0.1, 0.1)
plt.xlim(0.5,2.5)
plt.ylabel('latency (ms)')

h, p=stats.ranksums(start_constriction.loc[0:5] , start_constriction.loc[6:10] )
print(h, p)


plt.figure()
m1=start_constriction2.loc[0:5].mean()
m2=start_constriction2.loc[6:10].mean()
sem1=stats.sem(start_constriction2.loc[0:5],axis=0)
sem2=stats.sem(start_constriction2.loc[6:10],axis=0)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
#plt.ylim(-0.1, 0.1)
plt.xlim(0.5,2.5)
plt.ylabel('latency (ms)')

h, p=stats.ranksums(start_constriction2.loc[0:5] , start_constriction2.loc[6:10] )
print(h, p)



    
plt.figure()
m1=CAmpl[['C1','C2','C3','C4','C5','C6']].mean()
m2=CAmpl[['M1','M2','M3','M4','M5']].mean()
sem1=stats.sem(CAmpl[['C1','C2','C3','C4','C5','C6']],axis=0)
sem2=stats.sem(CAmpl[['M1','M2','M3','M4','M5']],axis=0)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
plt.xlim(0.5,2.5)
plt.ylabel('Amplitude')

statistic, p=stats.ranksums(CAmpl[['C1','C2','C3','C4','C5','C6']] , CAmpl[['M1','M2','M3','M4','M5']] )
print(statistic, p)


plt.figure()
m1=CAmpl_rl[['C1','C2','C3','C4','C5','C6']].mean()
m2=CAmpl_rl[['M1','M2','M3','M4','M5']].mean()
sem1=stats.sem(CAmpl_rl[['C1','C2','C3','C4','C5','C6']],axis=0)
sem2=stats.sem(CAmpl_rl[['M1','M2','M3','M4','M5']],axis=0)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
plt.xlim(0.5,2.5)
plt.ylabel('Amplitude rl')

statistic, p=stats.ranksums(CAmpl_rl[['C1','C2','C3','C4','C5','C6']] , CAmpl_rl[['M1','M2','M3','M4','M5']] )
print(statistic, p)



constriction_time=[]
for i in range(0,10):
    constriction_time.append(Dm_idx[i].astype(float)*(1000/125)-start_constriction[i])

cons_time_series=pd.Series(constriction_time)
plt.figure()
m1=cons_time_series.loc[0:5].mean()
m2=cons_time_series.loc[6:10].mean()
sem1=stats.sem(cons_time_series.loc[0:5],axis=0)
sem2=stats.sem(cons_time_series.loc[6:10],axis=0)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
plt.xlim(0.5,2.5)
plt.ylabel('Constriction time')

ctrl=q[['C1','C2','C3','C4','C5','C6']]
mut=q[['M1','M2','M3','M4','M5']]

plt.figure()
ax1_cs=q[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(kind='line')
qx=range(399)
qy=q[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
qy_sem=q[['C1','C2','C3','C4','C5','C6']].std(axis=1)
for j in range(1,399):
    qy_sem[j]=qy_sem[j]/math.sqrt(6)
plt.errorbar(qx,qy,qy_sem)
ax2_cs=q[['M1','M2','M3','M4','M5']].mean(axis=1).plot(kind='line')
qy=q[['M1','M2','M3','M4','M5']].mean(axis=1)
qy_sem=q[['M1','M2','M3','M4','M5']].std(axis=1)
for j in range(1,400):
    qy_sem[j]=qy_sem[j]/math.sqrt(5)
plt.errorbar(qx,qy,qy_sem)
plt.legend(['WT','Shank3'])
plt.suptitle("Luminance pupil response",fontsize=18)
plt.tight_layout(rect=[0, 0.1, 1, 0.95])

for timestep in range(0,399):
    #q[['C1','C2','C3','C4','C5','C6']].iloc[timestep]
    h, p=stats.ttest_ind(q[['C1','C2','C3','C4','C5','C6']].iloc[timestep].dropna() , q[['M1','M2','M3','M4','M5']].iloc[timestep].dropna() )
    print(timestep, p)
    if(p<0.05):
        plt.plot(timestep,0,'ro')







ctrl=q_minzero[['C1','C2','C3','C4','C5','C6']]
mut=q_minzero[['M1','M2','M3','M4','M5']]

plt.figure()

ax1_cs=q_minzero[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(kind='line',color='b')
qx=range(399)
qy=q_minzero[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
qy_sem1=q_minzero[['C1','C2','C3','C4','C5','C6']].std(axis=1)
for j in range(1,399):
    qy_sem1[j]=qy_sem1[j]/math.sqrt(6)
plt.errorbar(qx,qy,qy_sem1,ecolor='b')

ax2_cs=q_minzero[['M1','M2','M3','M4','M5']].mean(axis=1).plot(kind='line',color='g')
qy=q_minzero[['M1','M2','M3','M4','M5']].mean(axis=1)
qy_sem2=q_minzero[['M1','M2','M3','M4','M5']].std(axis=1)
for j in range(1,399):
    qy_sem2[j]=qy_sem2[j]/math.sqrt(5)
plt.errorbar(qx,qy,qy_sem2,ecolor='g')

plt.legend(['WT','Shank3'])
plt.suptitle("Luminance pupil response, mean",fontsize=18)
plt.tight_layout(rect=[0, 0.1, 1, 0.95])
plt.xticks([0, 125, 250, 375], [0, 1, 2, 3])
plt.xlabel('time after stim onset (s)')

for timestep in range(0,399):
    #q[['C1','C2','C3','C4','C5','C6']].iloc[timestep]
    h, p=stats.ranksums(q_minzero[['C1','C2','C3','C4','C5','C6']].iloc[timestep].dropna() , q_minzero[['M1','M2','M3','M4','M5']].iloc[timestep].dropna() )
    print(timestep, p)
    if(p<0.05):
        plt.plot(timestep,0,'ro')
        
        
        
        
q_minzero['MeanC']=q_minzero[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
q_minzero['SemC']=qy_sem1  
q_minzero['MeanM']=q_minzero[['M1','M2','M3','M4','M5']].mean(axis=1)
q_minzero['SemM']=qy_sem2

plt.figure()
q_minzero['MeanC'].plot(kind='line',color='b')
plt.errorbar(qx,q_minzero['MeanC'],qy_sem1,ecolor='b')  
q_minzero['MeanM'].plot(kind='line',color='r')
plt.errorbar(qx,q_minzero['MeanM'],qy_sem2,ecolor='r')    
         

str1= 'E:\\Dropbox (MIT)\\Presentations and Writings\\Shank3 macaque manuscript\\excel_data\\Pupil_reflect_export2.xlsx'
writer = ExcelWriter(str1)
q_minzero.to_excel(writer,'Sheet5')
writer.save()



# Here we're going to plot fraction watched, per emo category, per round, per genetic status

# In[4]:

fig, axes = plt.subplots(nrows=2, ncols=3)
ax1=df_fractwatched_1[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(ax=axes[0,0], ylim=[0, 1], kind='bar',title='WT round 1')
ax2=df_fractwatched_1[['M1','M2','M3','M4','M5']].mean(axis=1).plot(ax=axes[1,0], ylim=[0, 1], kind='bar',title='Shank3 round 1')
ax1.set_xticklabels(['sub','neu','thr'],rotation=0)
ax2.set_xticklabels(['sub','neu','thr'],rotation=0)
ax1.set_ylim(0.25,0.65)
ax2.set_ylim(0.45,0.65)

ax3=df_fractwatched_2[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(ax=axes[0,1], ylim=[0, 1], kind='bar',title='WT round 2')
ax4=df_fractwatched_2[['M1','M2','M3','M4','M5']].mean(axis=1).plot(ax=axes[1,1], ylim=[0, 1], kind='bar',title='Shank3 round 2')
ax3.set_xticklabels(['sub','neu','thr'],rotation=0)
ax4.set_xticklabels(['sub','neu','thr'],rotation=0)
ax3.set_ylim(0.25,0.65)
ax4.set_ylim(0.45,0.65)
#plt.tight_layout()

ax5=df_fractwatched_3[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(ax=axes[0,2], ylim=[0, 1], kind='bar',title='WT round 3')
ax6=df_fractwatched_3[['M1','M2','M3','M4','M5']].mean(axis=1).plot(ax=axes[1,2], ylim=[0, 1], kind='bar',title='Shank3 round 3')
ax5.set_xticklabels(['sub','neu','thr'],rotation=0)
ax6.set_xticklabels(['sub','neu','thr'],rotation=0)
ax5.set_ylim(0.25,0.65)
ax6.set_ylim(0.45,0.65)

plt.suptitle("Fraction watched",fontsize=18)
plt.tight_layout(rect=[0, 0.1, 1, 0.95])


# Fraction watched, mean across the 3 rounds

# In[5]:

df_concat0 = pd.concat((df_fractwatched_1, df_fractwatched_2), axis=0)
d=df_concat0.groupby(level=0).mean()

fig, axes = plt.subplots(nrows=1, ncols=2)
m1=d[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
sem1=stats.sem(d[['C1','C2','C3','C4','C5','C6']].mean(axis=1))
ax1=m1.plot(ax=axes[0], ylim=[0, 1], kind='bar',title='WT',yerr=sem1)
m2=d[['M1','M2','M3','M4','M5']].mean(axis=1)
sem2=stats.sem(d[['M1','M2','M3','M4','M5']].mean(axis=1))
ax2=m2.plot(ax=axes[1], ylim=[0, 1], kind='bar',title='Shank3',yerr=sem2)
ax1.set_xticklabels(['sub','neu','thr'],rotation=0)
ax2.set_xticklabels(['sub','neu','thr'],rotation=0)
ax1.set_ylim(0.3,0.6)
ax2.set_ylim(0.3,0.6)
plt.suptitle("Fraction watched, mean",fontsize=18)
plt.tight_layout(rect=[0, 0.1, 1, 0.95])

str1= dir1 + 'Fract_watched_export.xlsx'
writer = ExcelWriter(str1)
d.to_excel(writer,'Sheet5')
writer.save()

#save d

#save to hdf5
hdf_name=dir1+'fract_watched_only.h5'
if os.path.isfile(hdf_name):
    os.remove(hdf_name)
        
hdf = pd.HDFStore(hdf_name)
d.to_hdf(hdf_name, 'd', table=True, mode='a',complevel=9)
hdf.close()
        










#zoom in on y axis ...
fig, axes = plt.subplots(nrows=1, ncols=2)
m1=d[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
sem1=stats.sem(d[['C1','C2','C3','C4','C5','C6']].mean(axis=1))
ax1=m1.plot(ax=axes[0], kind='bar',title='WT',yerr=sem1)
m2=d[['M1','M2','M3','M4','M5']].mean(axis=1)
sem2=stats.sem(d[['M1','M2','M3','M4','M5']].mean(axis=1))
ax2=m2.plot(ax=axes[1], kind='bar',title='Shank3',yerr=sem2)
ax1.set_xticklabels(['sub','neu','thr'],rotation=0)
ax2.set_xticklabels(['sub','neu','thr'],rotation=0)
ax1.set_ylim(0.3,0.6)
ax2.set_ylim(0.5,0.6)
plt.suptitle("Fraction watched, mean",fontsize=18)
plt.tight_layout(rect=[0, 0.1, 1, 0.95])


# Pupil response

# In[25]:

df_pup_ag = pd.concat((df_pupresult_1_ag, df_pupresult_2_ag, df_pupresult_3_ag), axis=0)
d_ag_m=df_pup_ag.groupby(level=0).mean()

df_pup_ne = pd.concat((df_pupresult_1_ne, df_pupresult_2_ne, df_pupresult_3_ne), axis=0)
d_ne_m=df_pup_ne.groupby(level=0).mean()

df_pup_su = pd.concat((df_pupresult_1_su, df_pupresult_2_su, df_pupresult_3_su), axis=0)
d_su_m=df_pup_su.groupby(level=0).mean()

dfs[0]=d_ag_m
dfs[1]=d_ne_m
dfs[2]=d_su_m
panel = pd.Panel(dfs)
q=panel.mean(axis=0)

ctrl=q[['C1','C2','C3','C4','C5','C6']]
mut=q[['M1','M2','M3','M4','M5']]

plt.figure()
ax1_cs=q[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(kind='line')
ax2_cs=q[['M1','M2','M3','M4','M5']].mean(axis=1).plot(kind='line')
plt.legend(['WT','Shank3'])
plt.suptitle("Pupil response, mean",fontsize=18)
plt.tight_layout(rect=[0, 0.1, 1, 0.95])
plt.xlim(0, 50)

for timestep in range(0,50):
    #q[['C1','C2','C3','C4','C5','C6']].iloc[timestep]
    h, p=stats.ttest_ind(q[['C1','C2','C3','C4','C5','C6']].iloc[timestep].dropna() , q[['M1','M2','M3','M4','M5']].iloc[timestep].dropna() )
    print(timestep, p)
    if(p<0.05):
        plt.plot(timestep,0,'ro')
    
#cat1 = q[q['Category']=='cat1']
#cat2 = q[q['Category']=='cat2']

#ttest_ind(cat1['values'], cat2['values'])

#selecting row 1, column 'A'
#df_test['A'].iloc[0]
#df_test.iloc[0]



# Pupil response per emo category, plotted in two ways

# In[10]:


fig, axes = plt.subplots(nrows=1, ncols=2)
ax1ag=d_ag_m[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(ax=axes[0], xlim=[0, 50], ylim=[-1, 1], kind='line',title='WT')
ax1ne=d_ne_m[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(ax=axes[0], xlim=[0, 50], ylim=[-1, 1], kind='line',title='WT')
ax1su=d_su_m[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(ax=axes[0], xlim=[0, 50], ylim=[-1, 1], kind='line',title='WT')

ax2ag=d_ag_m[['M1','M2','M3','M4','M5']].mean(axis=1).plot(ax=axes[1], xlim=[0, 50], ylim=[-1, 1], kind='line',title='Shank3')
ax2ne=d_ne_m[['M1','M2','M3','M4','M5']].mean(axis=1).plot(ax=axes[1], xlim=[0, 50], ylim=[-1, 1], kind='line',title='Shank3')
ax2su=d_su_m[['M1','M2','M3','M4','M5']].mean(axis=1).plot(ax=axes[1], xlim=[0, 50], ylim=[-1, 1], kind='line',title='Shank3')
#ax1.set_xticklabels(['sub','neu','thr'],rotation=0)
#ax2.set_xticklabels(['sub','neu','thr'],rotation=0)
#ax1.set_ylim(0.3,0.4)
#ax2.set_ylim(0.5,0.6)
axes[0].legend(['ag','ne','su'])
axes[1].legend(['ag','ne','su'])
#ax1ne.legend(['ne'])

plt.suptitle("Pupil response",fontsize=18)
plt.tight_layout(rect=[0, 0.3, 1, 0.95])


fig, axes = plt.subplots(nrows=1, ncols=3)
ax1ag=d_ag_m[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(ax=axes[0], xlim=[0, 50], ylim=[-1, 1], kind='line',title='AG')
ax1ne=d_ne_m[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(ax=axes[1], xlim=[0, 50], ylim=[-1, 1], kind='line',title='NE')
ax1su=d_su_m[['C1','C2','C3','C4','C5','C6']].mean(axis=1).plot(ax=axes[2], xlim=[0, 50], ylim=[-1, 1], kind='line',title='SU')

ax2ag=d_ag_m[['M1','M2','M3','M4','M5']].mean(axis=1).plot(ax=axes[0], xlim=[0, 50], ylim=[-1, 1], kind='line',title='AG')
ax2ne=d_ne_m[['M1','M2','M3','M4','M5']].mean(axis=1).plot(ax=axes[1], xlim=[0, 50], ylim=[-1, 1], kind='line',title='NE')
ax2su=d_su_m[['M1','M2','M3','M4','M5']].mean(axis=1).plot(ax=axes[2], xlim=[0, 50], ylim=[-1, 1], kind='line',title='SU')
#ax1.set_xticklabels(['sub','neu','thr'],rotation=0)
#ax2.set_xticklabels(['sub','neu','thr'],rotation=0)
#ax1.set_ylim(0.3,0.4)
#ax2.set_ylim(0.5,0.6)
axes[0].legend(['WT','Shank3'])
axes[1].legend(['WT','Shank3'])
axes[2].legend(['WT','Shank3'])
#ax1ne.legend(['ne'])

plt.suptitle("Pupil response by content",fontsize=18)
plt.tight_layout(rect=[0, 0.3, 1, 0.95])





# Tonic Pupil size
# 
# 
# MUSt average across all rounds
# 

# In[61]:

#df_meanpup1[['C1','C2','C3','C4','C5','C6']]
# print(df_meanpup1)
# print(df_meanpup2)
# print(df_meanpup3)

df_meanpup_neu_thr=pd.DataFrame()
dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Neutral_v_threat\\'
for animal_ID in IDS:
    str1= dir1 + animal_ID + '.h5'
    df_fract_neu_thr=pd.read_hdf(str1,'df_fract')
    df_meanpup_neu_thr[animal_ID]=df_fract_neu_thr['meanpupil']  

print(df_meanpup_neu_thr)   
df_concat = pd.concat((df_meanpup1, df_meanpup2,df_meanpup3,df_meanpup_neu_thr))
#print df_concat.mean()
m=df_concat.mean()
m1=m[['C1','C2','C3','C4','C5','C6']].mean(axis=0)
m2=m[['M1','M2','M3','M4','M5']].mean(axis=0)
sem1=stats.sem(m[['C1','C2','C3','C4','C5','C6']],axis=0)
sem2=stats.sem(m[['M1','M2','M3','M4','M5']],axis=0)
m3 = pd.DataFrame(columns=[''], index=[0,1])
m3.loc[0] = m1
m3.loc[1] = m2
fig, axes = plt.subplots(nrows=1,ncols=2)
#ax2=m3.plot(ax=axes[0], ylim=[3, 4], kind='bar',title='tonic pupil',yerr=sem3,legend=False)


# In[28]:



fig, axes = plt.subplots(nrows=1,ncols=2)
m1=df_meanpup1[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
m2=df_meanpup2[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
m3=df_meanpup3[['C1','C2','C3','C4','C5','C6']].mean(axis=1)
sem1=stats.sem(df_meanpup1[['C1','C2','C3','C4','C5','C6']],axis=1)
sem2=stats.sem(df_meanpup2[['C1','C2','C3','C4','C5','C6']],axis=1)
sem3=stats.sem(df_meanpup3[['C1','C2','C3','C4','C5','C6']],axis=1)



m2=df_meanpup3[['M1','M2','M3','M4','M5']].mean(axis=1)
sem2=stats.sem(df_meanpup3[['M1','M2','M3','M4','M5']],axis=1)

m3 = pd.DataFrame(columns=[''], index=[0,1])
m3.loc[0] = m1[0]
m3.loc[1] = m2[0]
sem3 = pd.DataFrame(columns=[''], index=[0,1])
sem3.loc[0] = sem1[0]
sem3.loc[1] = sem2[0]

ax2=m3.plot(ax=axes[0], ylim=[3, 4], kind='bar',title='tonic pupil',yerr=sem3,legend=False)
ax2.set_xticklabels(['WT','Shank3'],rotation=0)
plt.tight_layout()
a1=df_meanpup3.as_matrix(columns={'M1','M2','M3','M4','M5'})
a1=np.reshape(a1, (5, 1))
a2=df_meanpup3.as_matrix(columns={'C1','C2','C3','C4','C5','C6'})
a2=np.reshape(a2, (6, 1))
t,p = stats.ttest_ind(a1, a2)  
print("ttest tonic pupil size:            t = %g  p = %g" % (t, p))


# In[27]:

df_meanpup3[['C1','C2','C3','C4','C5','C6']].iloc[1]

