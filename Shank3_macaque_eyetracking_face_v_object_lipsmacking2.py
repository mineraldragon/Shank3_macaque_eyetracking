

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
import re

teller=-1
elapsed=[]
IDS=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5']
#IDS=['M3']

# Loading animals one by one
# df_fract =  only mean values for pupil size and fraction watched per emo cat
# df_cum1 = pupil response any time there was a face
# df_pupresult = pupil response for ag, ne and su
# df1edia = fraction watched, per clip
# df_all = everything

# In[3]:
    
#datafile='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Lipsmacking_second_round\\matlab_lipsmacking_data_M3_redo.csv'
datafile='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Face_v_Object\\Lipsmacking Face_vs_Object - C1 - M5 - Event Logs.csv'
lipsmack_data = pd.read_csv(datafile,sep=',')

eyetrack_vs_lipsmack_lag = {'animal_ID': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5'], 'lag': [0, 24, 21, 35, 59, 33, 52, 180, 35, 74, 48]}
df_lag = pd.DataFrame(data=eyetrack_vs_lipsmack_lag)


# body_d, face_d, bodylook_d, facelook_d
c = ['animal_ID', 'eyes_on_screen_d', 'not_eyes_on_screen_d','lipsmacking_d', 'eyes_on_screen_and_lipsmacking_d',  'face_d', 'looking_at_face_d', 'looking_at_object_d', 'ratio_eyes_on_screen_and_lipsmacking', 'ratio_not_eyes_on_screen_and_lipsmacking',  'looking_at_face_and_lipsmacking_d', 'looking_at_object_and_lipsmacking_d', 'ratio_looking_at_face', 'ratio_looking_at_object']
            
df_lipsmacking=pd.DataFrame(np.nan,index=[0],columns=c)
#dataframe[columns:animal,set,medianame,eyes_on_screen_d, was_lipsmacking_d, etc]
teller1=0;

for animal_ID in IDS:
    
    startpoint = time.time()
    teller=teller+1
    print(teller)

    dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Face_v_Object\\'
    str1= dir1 + animal_ID + '.h5'
    
    #now we have already selected the animal
    df1=pd.read_hdf(str1,'df')

    qq=df_lag.loc[df_lag['animal_ID'] == animal_ID,'lag'].iloc[0]
    lipsmack_data.loc[:,'time_ms']= (lipsmack_data['Time_Relative_sf'] * 1000) - (qq * 1000)
     
        #select lipsmack observations for animal
    lipsmack_this=lipsmack_data[lipsmack_data['Observation'].str.contains(animal_ID)]
    lipsmack_this = lipsmack_this.reset_index(drop=True)
    df1['lipsmack']=0
    
    for i in range(0,(lipsmack_this.shape[0]-1)):
        
        if((i % 2)==0):
            #find indices with values closest to 'time_ms' start (i) and stop (i+1)
            idx1 = (np.abs(df1['RecordingTimestamp'] - lipsmack_this.loc[i,'time_ms'])).argmin()
            idx2 = (np.abs(df1['RecordingTimestamp'] - lipsmack_this.loc[i+1,'time_ms'])).argmin()
            
            #make values in that range 1
            df1.loc[idx1:idx2,'lipsmack']=1
                   
              
    was_lipsmacking=df1['lipsmack'] == 1 #monkey was lipsmacking   
    was_lipsmacking_d=len(was_lipsmacking[(was_lipsmacking==1)]) #duration of looking in samples   
            



#screen

            
    #samples where the monkey was looking
    eyes_on_screen=df1.eyes_on_screen #true when looking
    not_eyes_on_screen=df1.eyes_on_screen==0 #true when looking
    eyes_on_screen_d=len(eyes_on_screen[(eyes_on_screen==1)]) #duration of looking in samples
    not_eyes_on_screen_d=len(eyes_on_screen[(eyes_on_screen==0)]) #duration of looking in samples
    
    was_lipsmacking=df1['lipsmack'] == 1 #monkey was lipsmacking   
  
    was_lipsmacking_d=len(was_lipsmacking[(was_lipsmacking==1)]) #duration of looking in samples   
    lipsmack_latency=-1
    if(was_lipsmacking_d>0):
        d=was_lipsmacking.index[was_lipsmacking == True].tolist()
        lipsmack_latency=min(d)
        
    
    
    eyes_on_screen_and_lipsmacking=eyes_on_screen & was_lipsmacking  #true when looking and lipsmacking
    eyes_on_screen_and_lipsmacking_d=len(eyes_on_screen_and_lipsmacking[(eyes_on_screen_and_lipsmacking==1)]) 

    if(eyes_on_screen_d>0):
        ratio_eyes_on_screen_and_lipsmacking = float(eyes_on_screen_and_lipsmacking_d) / eyes_on_screen_d

    not_eyes_on_screen_and_lipsmacking=not_eyes_on_screen & was_lipsmacking  #true when looking and lipsmacking
    not_eyes_on_screen_and_lipsmacking_d=len(not_eyes_on_screen_and_lipsmacking[(not_eyes_on_screen_and_lipsmacking==1)]) 

    if(not_eyes_on_screen_d>0):
        ratio_not_eyes_on_screen_and_lipsmacking = float(not_eyes_on_screen_and_lipsmacking_d) / not_eyes_on_screen_d



#face


      
    face=df1.index[df1['face'] >= 0].tolist() #face was shown
    face_d=len(face)
    
    looking_at_face=df1['face'] == 1 #monkey was looking at face
    looking_at_face_d=len(looking_at_face[(looking_at_face==1)])

    tmp1=was_lipsmacking & looking_at_face #looking at body and lipsmacking
    looking_at_face_and_lipsmacking_d=len(tmp1[(tmp1==1)])
   
    ratio_looking_at_face=np.nan
    if(face_d>0 and looking_at_face_d>0):
        ratio_looking_at_face= float(looking_at_face_and_lipsmacking_d)/ looking_at_face_d
    
    
    object1=df1.index[df1['object'] >= 0].tolist() #face was shown
    object1_d=len(object1)
    looking_at_object=df1['object'] == 1 #monkey was looking at face

    looking_at_object_d=len(looking_at_object[(looking_at_object==1)])

    tmp1 = was_lipsmacking & looking_at_object #looking at body and lipsmacking
    looking_at_object_and_lipsmacking_d = len(tmp1[(tmp1==1)])
    
    ratio_looking_at_object=np.nan
    if(object1_d>0 and looking_at_object_d>0):
        ratio_looking_at_object= float(looking_at_object_and_lipsmacking_d)/ looking_at_object_d            

            
      
       
    df_tmp = pd.DataFrame([[animal_ID, eyes_on_screen_d, not_eyes_on_screen_d, was_lipsmacking_d, eyes_on_screen_and_lipsmacking_d, face_d,  looking_at_face_d, looking_at_object_d, ratio_eyes_on_screen_and_lipsmacking, ratio_not_eyes_on_screen_and_lipsmacking,  looking_at_face_and_lipsmacking_d, looking_at_object_and_lipsmacking_d, ratio_looking_at_face, ratio_looking_at_object]], columns=c)
            
    df_lipsmacking=df_lipsmacking.append(df_tmp, ignore_index=True)
            
            
            
            
            
            
            
            
            #calculate results
  
#%%

columns1=['animal_ID', 'face','object', 'screen', 'not_screen']

df_ratios=pd.DataFrame(np.nan,index=[0],columns=columns1)

for animal_ID in IDS:
    
    tmp1 = df_lipsmacking[(df_lipsmacking.animal_ID == animal_ID)] #dataframe
    
    ratio_face_ls=tmp1['ratio_looking_at_face'].mean()
    ratio_object_ls=tmp1['ratio_looking_at_object'].mean()

    print('\n\n\nanimal_ID:   ' +  animal_ID + '\n')
    
    print('face ' +  str(ratio_face_ls))
    print('object ' +  str(ratio_object_ls))
        
    ratio_screen_ls=tmp1['ratio_eyes_on_screen_and_lipsmacking'].mean()
    ratio_not_screen_ls=tmp1['ratio_not_eyes_on_screen_and_lipsmacking'].mean()
    
    print('screen ' +  str(ratio_screen_ls))
    print('not screen ' +  str(ratio_not_screen_ls))
    
    df_tmp = pd.DataFrame([[animal_ID, ratio_face_ls, ratio_object_ls, ratio_screen_ls, ratio_not_screen_ls]], columns=columns1)

    df_ratios=df_ratios.append(df_tmp, ignore_index=True)



#%%




cf=df_ratios[ ['face', 'object'] ].iloc[ [1,2,3,4,5,6] ]
mf=df_ratios[ ['face','object'] ].iloc[ [7,8,9,10,11] ]

plt.figure()
m1=cf.mean()
m2=mf.mean()
sem1=stats.sem(cf,axis=0)
sem2=stats.sem(mf,axis=0)
plt.errorbar([1, 2],m1,yerr=sem1, fmt='o')
plt.errorbar([1, 2],m2,yerr=sem2, fmt='o')
plt.xticks([1, 2],['face','object'])
#plt.xlim(0.5,2.5)
plt.ylabel('Fraction time lipsmacking')

statistic, p=stats.ranksums(mf['face'], mf['object'])
print(statistic, p)



plt.figure()
mf=mf.T
mf.plot()
plt.xticks([0, 1],['Face','object'])
plt.xlim(-0.5,1.5)
plt.ylabel('Fraction time lipsmacking')


cf=df_ratios[ ['face', 'object'] ].iloc[ [1,2,3,4,5,6] ]
mf=df_ratios[ ['face','object'] ].iloc[ [7,8,9,10,11] ]

res1=cf.append(mf)

plt.figure()
N = 11
ind = np.arange(N) 
width = 0.35       
plt.bar(ind,res1['face'],width,label='fixating face')
plt.bar(ind+width,res1['object'],width,label='fixating object')
plt.ylabel('Fraction time lipsmacking')
plt.title('Lipsmacking/grimacing during eye tracking')
plt.xticks(ind + width / 2, ('C1', 'C2', 'C3', 'C4', 'C5','C6','M1','M2','M3','M4','M5'))
plt.legend(loc='best')
plt.show()


str1= 'E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Face_v_Object\\Lipsmacking Face_vs_Object.xlsx'
writer = ExcelWriter(str1)
res1.to_excel(writer,'Sheet1')
writer.save()





cf=df_ratios[ ['screen', 'not_screen'] ].iloc[ [1,2,3,4,5,6] ]
mf=df_ratios[ ['screen','not_screen'] ].iloc[ [7,8,9,10,11] ]

plt.figure()
m1=cf.mean()
m2=mf.mean()
sem1=stats.sem(cf,axis=0)
sem2=stats.sem(mf,axis=0)
plt.errorbar([1, 2],m1,yerr=sem1, fmt='o')
plt.errorbar([1, 2],m2,yerr=sem2, fmt='o')
plt.xticks([1, 2],['screen','not_screen'])
#plt.xlim(0.5,2.5)
plt.ylabel('Fraction time lipsmacking')

statistic, p=stats.ranksums(mf['screen'], mf['not_screen'])
print(statistic, p)

#mf=mf.T
#cf=cf.T
res=cf.append(mf)
res=res.T
plt.figure()
res.plot()
plt.xticks([0, 1],['screen','not screen'])
plt.xlim(-0.5,1.5)
plt.ylabel('Fraction time lipsmacking')







