
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




teller=-1
elapsed=[]
IDS=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5']
#IDS=['C1']
C=['Xvar','Yvar']


df_Face_v_Object=pd.DataFrame(np.nan,index=IDS,columns=C)
df_Neutral_v_Threat=pd.DataFrame(np.nan,index=IDS,columns=C)

# Loading animals one by one
# df_fract =  only mean values for pupil size and fraction watched per emo cat
# df_cum1 = pupil response any time there was a face
# df_pupresult = pupil response for ag, ne and su
# df_media = fraction watched, per clip
# df_all = everything



for animal_ID in IDS:
    
    startpoint = time.time()
    teller=teller+1
    print(teller)

    for round1 in range(0,2):        

        if(round1==0):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Face_v_Object\\'
            str1= dir1 + animal_ID + '.tsv'
            df = pd.read_csv(str1,sep='\t') #read tsv into dataframe
        if(round1==1):
            dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Neutral_v_threat\\'
            str1= dir1 + animal_ID + '_Neut_v_emo.tsv'
            df = pd.read_csv(str1,sep='\t') #read tsv into dataframe

    
        df_fix_only = df[df['FixationIndex'].notnull()]
        
        if(round1==0):
            df_Face_v_Object.loc[animal_ID, 'Xvar'] = df_fix_only.loc[:,'GazePointX (ADCSpx)'].std()
            df_Face_v_Object.loc[animal_ID, 'Yvar'] = df_fix_only.loc[:,'GazePointY (ADCSpx)'].std()
        if(round1==1):
            df_Neutral_v_Threat.loc[animal_ID, 'Xvar'] = df_fix_only.loc[:,'GazePointX (ADCSpx)'].std()
            df_Neutral_v_Threat.loc[animal_ID, 'Yvar'] = df_fix_only.loc[:,'GazePointY (ADCSpx)'].std()
            
print(df_Face_v_Object)

print(df_Neutral_v_Threat)

plt.figure()
a1=df_Face_v_Object.loc[['C1','C2','C3','C4','C5','C6'],['Xvar']]
a2=df_Face_v_Object.loc[['M1','M2','M3','M4','M5'],['Xvar']]
m1=a1.mean(axis=0)
m2=a2.mean(axis=0)

sem1=stats.sem(a1)
sem2=stats.sem(a2)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1[0], sem2[0]], fmt='o')
plt.errorbar([1, 2],[m1, m2],yerr=[sem1[0], sem2[0]], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
plt.xlim(0.5,2.5)
plt.ylabel('fix std') 



plt.figure()
a1=df_Neutral_v_Threat.loc[['C1','C2','C3','C4','C5','C6'],['Xvar']]
a2=df_Neutral_v_Threat.loc[['M1','M2','M3','M4','M5'],['Xvar']]
m1=a1.mean(axis=0)
m2=a2.mean(axis=0)

sem1=stats.sem(a1)
sem2=stats.sem(a2)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1[0], sem2[0]], fmt='o')
plt.errorbar([1, 2],[m1, m2],yerr=[sem1[0], sem2[0]], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
plt.xlim(0.5,2.5)
plt.ylabel('fix std')     