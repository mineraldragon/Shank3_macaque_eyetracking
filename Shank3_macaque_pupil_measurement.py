
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
IDS=['C1', 'C2', 'C3', 'C4','C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5','CM003']


window_size_pre=1*120;
window_size_post=1*360;

startpoint = time.time()
teller=teller+1
print(teller)

nm='E:\\Dropbox (MIT)\\Baby macaques\\Preferential Looking Test\\Pupil_measurement.tsv'
df = pd.read_csv(nm,sep='\t') #read tsv into dataframe
  
#create column with pupil mean between pupil left and right        
df['meanpupil']=df[['PupilLeft', 'PupilRight']].mean(axis=1)  

#if one of them is nan, make mean nan too
#df.loc[df['PupilLeft'].isnull() & df['PupilRight'].isnull(),'meanpupil']=np.nan  

#If there is a value, that means the eyes are at the screen
df['eyes_on_screen'] = (df['GazePointX (ADCSpx)'] > 0) & (df['GazePointY (ADCSpx)'] > 0)

df_pupil_traces=pd.DataFrame()
df_means=pd.DataFrame()

#if there is a medianame

medias=df.MediaName
medias=medias[1:]
a=medias.str.contains('hite', regex=False) #white
a.fillna(False,inplace=True)
b=a.shape

#%%

list1=[]
for i in range(1,b[0]-1):
    if(a[i]==False and a[i+1]==True):
        list1.append(i+1)

df.ParticipantName.unique()

for animal in IDS:
    print(animal)
    df_pupil_traces=pd.DataFrame()
    ID=animal
    f=0
    for idx in list1:
        #print(ID)
        if(ID in df.ParticipantName[idx]):            
            f=f+1
            #surveys_df.loc[0, ['species_id', 'plot_id', 'weight']]
            
            q=df.loc[(idx-window_size_pre):(idx+window_size_post),'meanpupil']
            q.reset_index(inplace=True, drop=True)
            df_pupil_traces[f] = q
            #if ID=='M2':
            #    print(df.meanpupil[(idx-window_size_pre):(idx+window_size_post)])
    df_means[animal]=df_pupil_traces.mean(axis=1)

df_means.plot()
df_sub=df_means.iloc[1:120]

df_means=df_means-df_sub.mean()

ctrl=df_means[['C1', 'C2', 'C3', 'C4','C5', 'C6','CM003']].mean(axis=1)
mutant=df_means[['M1', 'M2', 'M3', 'M4', 'M5']].mean(axis=1)
x=range(0,df_means.shape[0])
plt.figure()
plt.plot(x,ctrl,color='k')
plt.plot(x,mutant,color='r')



medias=df.MediaName
medias=medias[1:]
a=medias.str.contains('lack', regex=False) #black
a.fillna(False,inplace=True)
b=a.shape
mpup=pd.DataFrame(index=[False, True], columns=IDS)
for animal in IDS:
    z= df[df['ParticipantName'].str.contains(animal)]
    if (z.empty == False):
        #print('it is not empty')
        #z.fillna(False,inplace=True)
        z.reset_index(drop=True,inplace=True)
        z['animal_black']=(z.MediaName.str.contains('lack') & z.ParticipantName.str.contains(animal))
        means=z.groupby('animal_black')['meanpupil'].mean()
        mpup[animal]=means
        #zz=z[z['MediaName'].str.contains('lack')]
        #mpup=z['meanpupil'].mea
 
z=df_means[:].iloc[340:381].mean(axis=0)
h, p=stats.ranksums(z[{'C1','C2','C3','C4','CM003','C6'}] , z[{'M1','M2','M3','M5'}] )
print(h, p)