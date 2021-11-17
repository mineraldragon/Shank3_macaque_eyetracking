

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

teller=-1
elapsed=[]
IDS=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5']
IDS=['M3']

# Loading animals one by one
# df_fract =  only mean values for pupil size and fraction watched per emo cat
# df_cum1 = pupil response any time there was a face
# df_pupresult = pupil response for ag, ne and su
# df_media = fraction watched, per clip
# df_all = everything

# In[3]:
    
datafile='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Lipsmacking_second_round\\matlab_lipsmacking_data.csv'
lipsmack_data = pd.read_csv(datafile,sep=',')

    

for animal_ID in IDS:
    
    startpoint = time.time()
    teller=teller+1
    print(teller)

    dir1='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Second_round\\'
    str1= dir1 + animal_ID + '.h5'
    
    #now we have already selected the animal
    df=pd.read_hdf(str1,'df')
    
    #remove unnecessary columns
    sel_cols = [col for col in df.columns if 'AOI' in col]
    df.drop(sel_cols, axis=1, inplace=True)

    sel_cols = [col for col in df.columns if 'Mouse' in col]
    df.drop(sel_cols, axis=1, inplace=True)    
    
    sel_cols = [col for col in df.columns if 'Scene' in col]
    df.drop(sel_cols, axis=1, inplace=True)      
    
    sel_cols = [col for col in df.columns if 'Segment' in col]
    df.drop(sel_cols, axis=1, inplace=True)  
    
    sel_cols = [col for col in df.columns if 'Gaze' in col]
    df.drop(sel_cols, axis=1, inplace=True)  

    sel_cols = [col for col in df.columns if 'EyePos' in col]
    df.drop(sel_cols, axis=1, inplace=True)  

    sel_cols = [col for col in df.columns if 'Cam' in col]
    df.drop(sel_cols, axis=1, inplace=True)     
    
    sel_cols = [col for col in df.columns if 'External' in col]
    df.drop(sel_cols, axis=1, inplace=True)      
    
    df=df.reset_index(drop=True)
    
            #for each clip: 
        #
        #-what part of the clip was the monkey actually looking?
        #-what proportion of looking time was the monkey lipsmacking?
        #-what category is the clip? group, filler, whole body, close up
        #   -subcategories of filler (close up of human or monkey y/n)
        #-
    
    for setn in range(1,4):    
    
        setstr='SET' + str(setn)
        #select only set 1
        df1=df[df['RecordingName'].str.contains(setstr)]
        #make indices start at 0
        df1=df1.reset_index(drop=True)
        
        #get names of clips shown in this set
        medias=df1.MediaName.unique()
        medias=medias[1:]
        

        
        
        
        
        
        
        #animal and set
        str1=animal_ID + ' SET '+ str(setn) 
        
        #select observations for animal and set
        lipsmack_this=lipsmack_data[lipsmack_data['Observation'].str.contains(str1)]
        #create column with nans
        lipsmack_this.loc[:,'time_ms']=np.nan
        lipsmack_this.loc[:,'time_ms']=lipsmack_this['Time_Relative_sf'] * 1000
        lipsmack_this = lipsmack_this.reset_index(drop=True)
        df1.loc[:,'lipsmack']=0
        
        for i in range(0,lipsmack_this.shape[0]):
            
            if((i % 2)==0):
                #find indices with values closest to 'time_ms' start (i) and stop (i+1)
                idx1 = (np.abs(df1['RecordingTimestamp'] - lipsmack_this.loc[i,'time_ms'])).argmin()
                idx2 = (np.abs(df1['RecordingTimestamp'] - lipsmack_this.loc[i+1,'time_ms'])).argmin()
                
                #make values in that range 1
                df1.loc[idx1:idx2,'lipsmack']=1
                
                
                
                

        
        
                
                
        tmp1=df1.index[df1['face'] >= 0].tolist() #face was shown
        tmp1look=df1.index[df1['face'] == 1].tolist() #monkey was looking at face
        tmp2=df1.index[df1['lipsmack'] == 1].tolist() #monkey was lipsmacking
        tmp3=list(set(tmp1) & set(tmp2)) #face on the screen and lipsmacking
        tmp4=list(set(tmp1look) & set(tmp2)) #looking at face and lipsmacking
        Lface=len(tmp1)
        Lface_look=len(tmp1look)
        Lface_ls=len(tmp3)
        Lface_look_ls=len(tmp4)      
        
        
        tmp1=df1.index[df1['body'] >= 0].tolist() #face was shown
        tmp1look=df1.index[df1['body'] == 1].tolist() #monkey was looking at face
        tmp2=df1.index[df1['lipsmack'] == 1].tolist() #monkey was lipsmacking
        tmp3=list(set(tmp1) & set(tmp2)) #face on the screen and lipsmacking
        tmp4=list(set(tmp1look) & set(tmp2)) #looking at face and lipsmacking
        Lbody=len(tmp1)
        Lbody_look=len(tmp1look)
        Lbody_ls=len(tmp3)
        Lbody_look_ls=len(tmp4)           
        
        L2=len(df1[(df1['body']>=0)])
        L3=len(df1[(df1['eyes_on_screen']>=0)])        

        
    
    
    #put in lipsmacking values
    

