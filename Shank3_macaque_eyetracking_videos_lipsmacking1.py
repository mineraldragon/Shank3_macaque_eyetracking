

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
#IDS=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5']
IDS=['M3']

# Loading animals one by one
# df_fract =  only mean values for pupil size and fraction watched per emo cat
# df_cum1 = pupil response any time there was a face
# df_pupresult = pupil response for ag, ne and su
# df_media = fraction watched, per clip
# df_all = everything

# In[3]:
    
datafile='E:\\Dropbox (MIT)\\Baby macaques\\Eyetracking\\Lipsmacking_second_round\\matlab_lipsmacking_data_M3_redo.csv'
lipsmack_data = pd.read_csv(datafile,sep=',')

eyetrack_vs_lipsmack_lag = {'animal_ID': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'M1', 'M2', 'M3', 'M4', 'M5'], 'lag_set1': [18, 38, 3, 26, 41, 0, 35, 20, 17, 20, 41], 'lag_set2': [62, 39, 136, 56, 130, 4, 158, 4, 45, 4,0], 'lag_set3': [36, 33, 34, 0, 37, 32, 24, 0, 33, 66, 41]}
df_lag = pd.DataFrame(data=eyetrack_vs_lipsmack_lag)


# body_d, face_d, bodylook_d, facelook_d
c = ['animal_ID', 'Set', 'MediaName','category1','category2','category3','category4','clip_duration','eyes_on_screen_d','lipsmacking_d', 'eyes_on_screen_and_lipsmacking_d', 'body_d', 'face_d', 'bodylook_d', 'facelook_d', 'looking_at_body_and_lipsmacking_d', 'looking_at_body_and_lipsmacking_d']
            
df_lipsmacking=pd.DataFrame(np.nan,index=[0],columns=c)
#dataframe[columns:animal,set,medianame,eyes_on_screen_d, was_lipsmacking_d, etc]
teller1=0;

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
    
    for setn in range(1,2):    
    
        setstr='SET' + str(setn)

        print(setstr)

        #select only set 1
        df1=df[df['RecordingName'].str.contains(setstr)]
        #make indices start at 0
        df1=df1.reset_index(drop=True)
        
        #get names of clips shown in this set
        medias=df1.MediaName.unique()
        medias=medias[1:]
        
        #animal and set
        str1=animal_ID + ' SET '+ str(setn) 
        
        #select lipsmack observations for animal and set
        lipsmack_this=lipsmack_data[lipsmack_data['Observation'].str.contains(str1)]
        #create column with nans
        lipsmack_this.loc[:,'time_ms']=np.nan
        
        qq=df_lag.loc[df_lag['animal_ID'] == animal_ID,'lag_set1'].iloc[0]
        lipsmack_this.loc[:,'time_ms']= (lipsmack_this['Time_Relative_sf'] * 1000) - (qq * 1000)
        
        
        lipsmack_this = lipsmack_this.reset_index(drop=True)
        df1.loc[:,'lipsmack']=0
        
        for i in range(0,lipsmack_this.shape[0]):
            
            if((i % 2)==0):
                #find indices with values closest to 'time_ms' start (i) and stop (i+1)
                idx1 = (np.abs(df1['RecordingTimestamp'] - lipsmack_this.loc[i,'time_ms'])).argmin()
                idx2 = (np.abs(df1['RecordingTimestamp'] - lipsmack_this.loc[i+1,'time_ms'])).argmin()
                
                #make values in that range 1
                df1.loc[idx1:idx2,'lipsmack']=1
                       
        #get the data for each clip..
        #first replace nans with str to avoid errors in the str comparison
        df1.MediaName = df1.MediaName.fillna('')
        mctr=0
        for m in medias:
            
            teller1=teller1+1;
            
            m=m.strip()
            m=m.replace(" ", "_")
            m=re.sub('[^A-Za-z0-9]+', '', m)
            m=m.lower()
            print(m)

            #create a single row dataframe for this cycle's data
            #df_lipsmacking_this_cycle=pd.DataFrame(np.nan,index=[0],columns=c)
            
            #start categorizing
            
            category1=''
            category2=''
            category3=''
            category4=''
            
            if(m.find('Whole_body_Ne')>0):
                category1='Whole_body'
                category2='ne'
                category3='Whole_body_ne'
                category4='face' #there is a close up face in it
                
            if(m.find('Whole_body_Su')>0):
                category1='Whole_body'
                category2='su'
                category3='Whole_body_su' 
                category4='face'
                
            if(m.find('Whole_body_Ag')>0):
                category1='Whole_body'
                category2='ag'
                category3='Whole_body_ag'
                category4='face'                
                
            if(m.find('Close_up_Ne')>0):
                category1='Close_up'
                category2='ne'
                category3='Close_up_ne'
                category4='face'
                
            if(m.find('Close_up_Su')>0):
                category1='Close_up'
                category2='su'
                category3='Close_up_su' 
                category4='face'
                
            if(m.find('Close_up_Ag')>0):
                category1='Close_up'
                category2='ag'
                category3='Close_up_ag'
                category4='face'                
                
            if(m.find('Group_aggression')>0):
                category1='Group'
                category2='aggression'
                category3='Group_aggression'
                category4='noface'
                
            if(m.find('Group_mounting')>0):
                category1='Group'
                category2='mounting'
                category3='Group_mounting' 
                category4='noface'
                
            if(m.find('Group_foraging')>0):
                category1='Group'
                category2='foraging'
                category3='Group_foraging'                
                category4='noface'
                
            if(m.find('Group_play')>0):
                category1='Group'
                category2='play'
                category3='Group_play'   
                category4='noface'
                
            if(m.find('Group_nonspecificSocial')>0):
                category1='Group'
                category2='nonspecificSocial'
                category3='Group_nonspecificSocial'   
                category4='noface'
                
            if(m.find('Group_grooming')>0):
                category1='Group'
                category2='grooming'
                category3='Group_grooming'   
                category4='noface'                
                
            if(m.find('Fillar')>0):
                category1='Filler'        
                category4='noface'
                
            if(m.find('Filler')>0):
                category1='Filler'   
                
            if(m=='Filler_Harold Lloyd - Safety Last! - Part 3 of 3 - YouTube_3_14.avi'):
                category4='face'
            if(m=='Filler_katyperry.4.avi'):
                category4='face'
            if(m=='Filler_Monkey Kingdom_2_36(1).avi'):
                category4='face'
            if(m=='Filler_Monkey Kingdom_2_43(1).avi'):
                category4='face'
            if(m=='Filler_Monkey Kingdom_2_49(1).avi'):
                category4='face'
            if(m=='Filler_Animal Atlas, School of Mammals - YouTube_2_20.avi'):
                category4='face'
            if(m=='Filler_BAKING A CAKE CHALLENGE - Merrell Twins (feat. Gabriel Conte) - YouTube_1_15.avi'):
                category4='face'
            if(m=='Filler_cavan.1.avi'):
                category4='face'                                        
            if(m=='Filler_cavan.2.avi'):
                category4='face'
            if(m=='Filler_Chaplin1.12.avi'):
                category4='face'
            if(m=='Filler_foli.25.avi'):
                category4='face'
            if(m=='Filler_Gangnam.1.avi'):
                category4='face'
            if(m=='Filler_Gangnam.4.avi'):
                category4='face'
            if(m=='Filler_foli.14.avi'):
                category4='face'
            if(m=="Filler_Stand Up, Sit Down Children's song by Patty Shukla (DVD Version) - YouTube_15.avi'"):
                category4='face'
            if(m=='Filler_Wheels on the Bus and More Nursery Rhymes by Mother Goose Club Playlist! - YouTube_10_8.avi'):
                category4='face'
            if(m=='Filler_Wheels on the Bus and More Nursery Rhymes by Mother Goose Club Playlist! - YouTube_10_24.avi'):
                category4='face'
            if(m=='Filler_Hoelahoep - Onderwater HD Aflevering 5 - YouTube_3_13.avi'):
                category4='face'
            if(m=='Filler_Monkey Kingdom_2_26.avi'):
                category4='face'
            if(m=='Filler_Monkeys Stealing Things (HD) [Funny Pets] - YouTube_3.avi'):
                category4='face'
            if(m=='Filler_DVD-Title1_1_11.avi'):
                category4='face'
            if(m=='Filler_Friends - Kind of a Loner Joey & Erin  Phoebe, Rachel - YouTube_21.avi'):
                category4='face'
            if(m=='Filler_BAKING A CAKE CHALLENGE - Merrell Twins (feat. Gabriel Conte) - YouTube_1_1.avi'):
                category4='face'
            if(m=='Filler_Itsy Bitsy Spider Nursery rhyme song for children (sung by Patty Shukla) - YouTube(00h00m23s-00h00m34s).avi'):
                category4='face'
            if(m=='Filler_Monkey Kingdom_2_54.avi'):
                category4='face'
            if(m=='Filler_Monkey LOVES French Fries! - YouTube_5.avi'):
                category4='face'
            if(m=='Filler_Friends - Kind of a Loner Joey & Erin  Phoebe, Rachel - YouTube_2.avi'):
                category4='face'
            if(m=='Filler_Pat-a-Cake  Mother Goose Club Playhouse Kids Video - YouTube_3.avi'):
                category4='face'
            if(m=="Filler_Stand Up, Sit Down Children's song by Patty Shukla (DVD Version) - YouTube_7.avi"):
                category4='face'
            if(m=='Filler_DVD-Title1_1_22.avi'):
                category4='face'
            if(m=='Filler_Untitled3.avi'):
                category4='face'
                    
                    
            #end categorizing        
               
            mctr=mctr+1;
            
            ##somehow not always a match...
            

            df_m=df1[df1['MediaName'].str.match(m)] #dataframe with everything incl lipsmacking for this clip
            df_m = df_m.reset_index(drop=True)
            
            print(df_m)
            
            #so, the number of rows for this dataframe is how long it was shown (in samples)
            clip_duration_smp=df_m.shape[0]
            
            #for each clip: 

            #-what part of the clip was the monkey actually looking?
            #-what proportion of looking time was the monkey lipsmacking?
            #-what category is the clip? group, filler, whole body, close up
            #   -subcategories of filler (close up of human or monkey y/n)
            
            #samples where the monkey was looking
            eyes_on_screen=df_m.eyes_on_screen #true when looking
            eyes_on_screen_d=len(eyes_on_screen[(eyes_on_screen==1)]) #duration of looking in samples
            
            was_lipsmacking=df_m['lipsmack'] == 1 #monkey was lipsmacking   
            was_lipsmacking_d=len(was_lipsmacking[(was_lipsmacking==1)]) #duration of looking in samples   
            
            eyes_on_screen_and_lipsmacking=eyes_on_screen & was_lipsmacking  #true when looking and lipsmacking
            eyes_on_screen_and_lipsmacking_d=len(eyes_on_screen_and_lipsmacking[(eyes_on_screen_and_lipsmacking==1)]) 

            body=df_m.index[df_m['body'] >= 0].tolist() #body was shown
            body_d=len(body)
            bodylook=df_m.index[df_m['body'] == 1].tolist() #monkey was looking at body
            bodylook_d=len(bodylook)
            
            face=df_m.index[df_m['face'] >= 0].tolist() #face was shown
            face_d=len(face)
            facelook=df_m.index[df_m['face'] == 1].tolist() #monkey was looking at face
            facelook_d=len(facelook)
            
            tmp1=list( set(was_lipsmacking) & set(bodylook) ) #looking at body and lipsmacking
            looking_at_body_and_lipsmacking_d=len(tmp1)
            
            tmp1=list( set(was_lipsmacking) & set(facelook) ) #looking at body and lipsmacking
            looking_at_face_and_lipsmacking_d=len(tmp1)
            
            df_tmp = pd.DataFrame([[animal_ID, setn, m, category1, category2, category3, category4, clip_duration_smp, eyes_on_screen_d, was_lipsmacking_d, eyes_on_screen_and_lipsmacking_d, body_d, face_d, bodylook_d, facelook_d, looking_at_body_and_lipsmacking_d, looking_at_face_and_lipsmacking_d]], columns=c)
            
            df_lipsmacking=df_lipsmacking.append(df_tmp, ignore_index=True)
            if(mctr==1):
                break
                        
        
