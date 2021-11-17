
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


     

dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Face_v_Object\\'
str1= dir1 + 'M1.tsv'
df1 = pd.read_csv(str1,sep='\t') #read tsv into dataframe

dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Neutral_v_threat\\'
str1= dir1 + 'M1_Neut_v_emo.tsv'
df2 = pd.read_csv(str1,sep='\t') #read tsv into dataframe
 
q1=df1.MediaName.unique()
q2=df2.MediaName.unique()


