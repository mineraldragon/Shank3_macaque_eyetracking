

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
c = ['animal_ID', 'Set', 'MediaName','category1','category2','category3','category4','clip_duration','eyes_on_screen_d', 'not_eyes_on_screen_d','lipsmacking_d', 'eyes_on_screen_and_lipsmacking_d', 'body_d', 'face_d', 'looking_at_body_d', 'not_looking_at_body_d', 'looking_at_face_d', 'not_looking_at_face_d', 'ratio_eyes_on_screen_and_lipsmacking', 'ratio_not_eyes_on_screen_and_lipsmacking', 'looking_at_body_and_lipsmacking_d', 'not_looking_at_body_and_lipsmacking_d', 'looking_at_face_and_lipsmacking_d', 'not_looking_at_face_and_lipsmacking_d', 'ratio_looking_at_body', 'ratio_not_looking_at_body', 'ratio_looking_at_face', 'ratio_not_looking_at_face']
            
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
    
    for setn in range(1,4):    
    
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
#        lipsmack_this.loc[:,'time_ms']=np.nan
        
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
        
        #df['E'] = df['B'].map(lambda x: re.sub(r'\W+', '', x))
        df1['MediaName'] = df1['MediaName'].map(lambda x: re.sub('[^A-Za-z0-9]+', '', x))
        df1['MediaName'] = df1['MediaName'].str.lower()
        
        
        mctr=0
        for m in medias:
            
#            if(mctr<=50):
            teller1=teller1+1;
            
            m=m.strip()
            #m=m.replace(" ", "_")
            m=re.sub('[^A-Za-z0-9]+', '', m)
            m=m.lower()
            #print(m)

            #create a single row dataframe for this cycle's data
            #df_lipsmacking_this_cycle=pd.DataFrame(np.nan,index=[0],columns=c)
            
            #start categorizing
            
            category1=''
            category2=''
            category3=''
            category4=''
            
            if(m.find('wholebodyne')>=0):
                category1='Whole_body'
                category2='ne'
                category3='Whole_body_ne'
                category4='face' #there is a close up face in it
                
            if(m.find('wholebodysu')>=0):
                category1='Whole_body'
                category2='su'
                category3='Whole_body_su' 
                category4='face'
                
            if(m.find('wholebodyag')>=0):
                category1='Whole_body'
                category2='ag'
                category3='Whole_body_ag'
                category4='face'                
                
            if(m.find('closeupne')>=0):
                category1='Close_up'
                category2='ne'
                category3='Close_up_ne'
                category4='face'
                
            if(m.find('closeupsu')>=0):
                category1='Close_up'
                category2='su'
                category3='Close_up_su' 
                category4='face'
                
            if(m.find('closeupag')>=0):
                category1='Close_up'
                category2='ag'
                category3='Close_up_ag'
                category4='face'                
                
            if(m.find('groupaggression')>=0):
                category1='Group'
                category2='aggression'
                category3='Group_aggression'
                category4='noface'
                
            if(m.find('groupmounting')>=0):
                category1='Group'
                category2='mounting'
                category3='Group_mounting' 
                category4='noface'
                
            if(m.find('groupforaging')>=0):
                category1='Group'
                category2='foraging'
                category3='Group_foraging'                
                category4='noface'
                
            if(m.find('groupplay')>=0):
                category1='Group'
                category2='play'
                category3='Group_play'   
                category4='noface'
                
            if(m.find('groupnonspecificsocial')>=0):
                category1='Group'
                category2='nonspecificSocial'
                category3='Group_nonspecificSocial'   
                category4='noface'

            if(m.find('groupneutral')>=0):
                category1='Group'
                category2='neutral'
                category3='Group_neutral'   
                category4='noface'
                
            if(m.find('groupgrooming')>=0):
                category1='Group'
                category2='grooming'
                category3='Group_grooming'   
                category4='noface'                
                
            if(m.find('fillar')>=0):
                category1='Filler'        
                category4='noface'
                
            if(m.find('filler')>=0):
                category1='Filler'   
                
            if(m=='fillerharoldlloydsafetylastpart3of3youtube314avi'):
                category4='face'
            if(m=='fillerkatyperry4avi'):
                category4='face'
            if(m=='fillermonkeykingdom2361avi'):
                category4='face'
            if(m=='fillermonkeykingdom2431avi'):
                category4='face'
            if(m=='fillermonkeykingdom2491avi'):
                category4='face'
            if(m=='filleranimalatlasschoolofmammalsyoutube220avi'):
                category4='face'
            if(m=='fillerbakingacakechallengemerrelltwinsfeatgabrielconteyoutube115avi'):
                category4='face'
            if(m=='fillerbakingacakechallengemerrelltwinsfeatgabrielconteyoutube11avi'):
                category4='face'
            if(m=='fillercavan1avi'):
                category4='face'                                        
            if(m=='fillercavan2avi'):
                category4='face'
            if(m=='fillerchaplin112avi'):
                category4='face'
            if(m=='fillerfoli25avi'):
                category4='face'
            if(m=='fillergangnam1avi'):
                category4='face'
            if(m=='fillergangnam4avi'):
                category4='face'
            if(m=='fillerfoli14avi'):
                category4='face'
            if(m=='fillerstandupsitdownchildrenssongbypattyshukladvdversionyoutube15avi'):
                category4='face'
            if(m=='fillerwheelsonthebusandmorenurseryrhymesbymothergooseclubplaylistyoutube108avi'):
                category4='face'
            if(m=='fillerwheelsonthebusandmorenurseryrhymesbymothergooseclubplaylistyoutube1024avi'):
                category4='face'
            if(m=='fillerhoelahoeponderwaterhdaflevering5youtube313avi'):
                category4='face'
            if(m=='fillermonkeykingdom226avi'):
                category4='face'
            if(m=='fillermonkeysstealingthingshdfunnypetsyoutube3avi'):
                category4='face'
            if(m=='fillerdvdtitle1111avi'):
                category4='face'
            if(m=='fillerfriendskindofalonerjoeyerinphoeberachelyoutube21avi'):
                category4='face'
            if(m=='fillerbakingacakechallengemerrelltwinsfeatgabrielconteyouTube11avi'):
                category4='face'
            if(m=='filleritsybitsyspidernurseryrhymesongforchildrensungbypattyshuklayoutube00h00m23s00h00m34savi'):
                category4='face'
            if(m=='fillermonkeykingdom254avi'):
                category4='face'
            if(m=='fillermonkeylovesfrenchfriesyoutube5avi'):
                category4='face'
            if(m=='fillerfriendskindofalonerjoeyerinphoeberachelyoutube2avi'):
                category4='face'
            if(m=='fillerpatacakemothergooseclubplayhousekidsvideoyoutube3avi'):
                category4='face'
            if(m=="fillerstandupsitdownchildrenssongbypattyshukladvdversionyoutube7avi"):
                category4='face'
            if(m=='fillerdvdtitle1122avi'):
                category4='face'
            if(m=='filleruntitled3avi'):
                category4='face'
                    
                    
            #end categorizing        
               
            mctr=mctr+1;
            
            ##somehow not always a match...
            

            df_m=df1[df1['MediaName'].str.match(m)] #dataframe with everything incl lipsmacking for this clip
            df_m = df_m.reset_index(drop=True)
            
      
            
            #print(df_m)
            
            #so, the number of rows for this dataframe is how long it was shown (in samples)
            clip_duration_smp=df_m.shape[0]
            
            #for each clip: 

            #-what part of the clip was the monkey actually looking?
            #-what proportion of looking time was the monkey lipsmacking?
            #-what category is the clip? group, filler, whole body, close up
            #   -subcategories of filler (close up of human or monkey y/n)
            
            #onset of looking
            #onset of lipsmacking
            
            
            #samples where the monkey was looking
            eyes_on_screen=df_m.eyes_on_screen #true when looking
            not_eyes_on_screen=df_m.eyes_on_screen==0 #true when looking
            eyes_on_screen_d=len(eyes_on_screen[(eyes_on_screen==1)]) #duration of looking in samples
            not_eyes_on_screen_d=len(eyes_on_screen[(eyes_on_screen==0)]) #duration of looking in samples
            
            was_lipsmacking=df_m['lipsmack'] == 1 #monkey was lipsmacking   
          
            was_lipsmacking_d=len(was_lipsmacking[(was_lipsmacking==1)]) #duration of looking in samples   
            lipsmack_latency=-1
            if(was_lipsmacking_d>0):
                d=was_lipsmacking.index[was_lipsmacking == True].tolist()
                lipsmack_latency=min(d)
                
            
            
            eyes_on_screen_and_lipsmacking=eyes_on_screen & was_lipsmacking  #true when looking and lipsmacking
            eyes_on_screen_and_lipsmacking_d=len(eyes_on_screen_and_lipsmacking[(eyes_on_screen_and_lipsmacking==1)]) 

            ratio_eyes_on_screen_and_lipsmacking = float(eyes_on_screen_and_lipsmacking_d) / eyes_on_screen_d

            not_eyes_on_screen_and_lipsmacking=not_eyes_on_screen & was_lipsmacking  #true when looking and lipsmacking
            not_eyes_on_screen_and_lipsmacking_d=len(not_eyes_on_screen_and_lipsmacking[(not_eyes_on_screen_and_lipsmacking==1)]) 

            ratio_not_eyes_on_screen_and_lipsmacking = float(not_eyes_on_screen_and_lipsmacking_d) / not_eyes_on_screen_d












#body

            body=df_m['body'] >= 0 #body was shown
            body_d=len(body[(body==1)])
            
            looking_at_body=df_m['body'] == 1 #monkey was looking at body
            looking_at_body_d=len(looking_at_body[(looking_at_body==1)])

            tmp1= was_lipsmacking & looking_at_body  #looking at body and lipsmacking
            looking_at_body_and_lipsmacking_d=len(tmp1[(tmp1==1)])
            
            ratio_looking_at_body=np.nan
            if(body_d>0 and looking_at_body_d>0):
                ratio_looking_at_body= float(looking_at_body_and_lipsmacking_d)/ looking_at_body_d


            not_looking_at_body=df_m['body'] == 0 
            not_looking_at_body_d=len(not_looking_at_body[(not_looking_at_body==1)])

            tmp1=was_lipsmacking & not_looking_at_body #looking at body and lipsmacking
            not_looking_at_body_and_lipsmacking_d=len(tmp1[(tmp1==1)])

            ratio_not_looking_at_body=np.nan
            if(body_d>0 and not_looking_at_body_d>0):
                ratio_not_looking_at_body= float(not_looking_at_body_and_lipsmacking_d)/ not_looking_at_body_d
            
            


#face            
            
            face=df_m.index[df_m['face'] >= 0].tolist() #face was shown
            face_d=len(face)
            
            looking_at_face=df_m['face'] == 1 #monkey was looking at face
            looking_at_face_d=len(looking_at_face[(looking_at_face==1)])

            tmp1=was_lipsmacking & looking_at_face #looking at body and lipsmacking
            looking_at_face_and_lipsmacking_d=len(tmp1[(tmp1==1)])
            
            ratio_looking_at_face=np.nan
            if(face_d>0 and looking_at_face_d>0):
                ratio_looking_at_face= float(looking_at_face_and_lipsmacking_d)/ looking_at_face_d
            
            not_looking_at_face=df_m['face'] == 0 
            not_looking_at_face_d=len(not_looking_at_face[(not_looking_at_face==1)])

            tmp1 = was_lipsmacking & not_looking_at_face #looking at body and lipsmacking
            not_looking_at_face_and_lipsmacking_d = len(tmp1[(tmp1==1)])
            
            ratio_not_looking_at_face=np.nan
            if(face_d>0 and not_looking_at_face_d>0):
                ratio_not_looking_at_face= float(not_looking_at_face_and_lipsmacking_d)/ not_looking_at_face_d            

            
            #this is all for individual media clips
            
            

            
            df_tmp = pd.DataFrame([[animal_ID, setn, m, category1, category2, category3, category4, clip_duration_smp, eyes_on_screen_d, not_eyes_on_screen_d, was_lipsmacking_d, eyes_on_screen_and_lipsmacking_d, body_d, face_d, looking_at_body_d, not_looking_at_body_d, looking_at_face_d, not_looking_at_face_d, ratio_eyes_on_screen_and_lipsmacking, ratio_not_eyes_on_screen_and_lipsmacking,looking_at_body_and_lipsmacking_d, not_looking_at_body_and_lipsmacking_d, looking_at_face_and_lipsmacking_d, not_looking_at_face_and_lipsmacking_d, ratio_looking_at_body, ratio_not_looking_at_body, ratio_looking_at_face, ratio_not_looking_at_face]], columns=c)
            
            df_lipsmacking=df_lipsmacking.append(df_tmp, ignore_index=True)
            
            
            
            
            
            
            
            
            #calculate results
            
#a=df_lipsmacking.shape[0]
#looking at a face - lipsmacking (fraction duration)  vs face shown but not looking - lipsmacking (fraction duration)
#looking at a body - lipsmacking (fraction duration)  vs body shown but not looking - lipsmacking (fraction duration)


#c = ['animal_ID', 'Set', 'MediaName','category1','category2','category3','category4','clip_duration','eyes_on_screen_d','lipsmacking_d', 'eyes_on_screen_and_lipsmacking_d', 'body_d', 'face_d', 'looking_at_body_d', 'looking_at_face_d']

#animal, looking at face
tmp1 = df_lipsmacking[(df_lipsmacking.animal_ID == 'M3')] #dataframe

ratio_face_ls=tmp1['ratio_looking_at_face'].mean()
ratio_not_face_ls=tmp1['ratio_not_looking_at_face'].mean()

print('face ' +  str(ratio_face_ls))
print('not face ' +  str(ratio_not_face_ls))

ratio_body_ls=tmp1['ratio_looking_at_body'].mean()
ratio_not_body_ls=tmp1['ratio_not_looking_at_body'].mean()

print('body ' +  str(ratio_body_ls))
print('not body ' +  str(ratio_not_body_ls))

ratio_screen_ls=tmp1['ratio_eyes_on_screen_and_lipsmacking'].mean()
ratio_not_screen_ls=tmp1['ratio_not_eyes_on_screen_and_lipsmacking'].mean()

print('screen ' +  str(ratio_screen_ls))
print('not screen ' +  str(ratio_not_screen_ls))


tmp1 = df_lipsmacking[(df_lipsmacking.category1 == 'Filler')]
ratio_filler_screen_ls=tmp1['ratio_eyes_on_screen_and_lipsmacking'].mean()
print('Filler screen ' +  str(ratio_filler_screen_ls))




tmp1 = df_lipsmacking.loc[(df_lipsmacking.category1 == 'Filler') & (df_lipsmacking.category4 == 'face')]
ratio_filler_face_screen_ls=tmp1['ratio_eyes_on_screen_and_lipsmacking'].mean()
print('Filler face screen ' +  str(ratio_filler_face_screen_ls))

tmp1 = df_lipsmacking.loc[(df_lipsmacking.category1 == 'Filler') & (df_lipsmacking.category4 == 'noface')]
ratio_filler_noface_screen_ls=tmp1['ratio_eyes_on_screen_and_lipsmacking'].mean()
print('Filler not face screen ' +  str(ratio_filler_noface_screen_ls))




tmp1 = df_lipsmacking[(df_lipsmacking.category1 == 'Group')]
ratio_group_screen_ls=tmp1['ratio_eyes_on_screen_and_lipsmacking'].mean()
print('Group screen ' +  str(ratio_group_screen_ls))

tmp1 = df_lipsmacking[(df_lipsmacking.category1 == 'Close_up')]
ratio_close_up_screen_ls=tmp1['ratio_eyes_on_screen_and_lipsmacking'].mean()
print('Close_up screen ' +  str(ratio_close_up_screen_ls))

tmp1 = df_lipsmacking[(df_lipsmacking.category1 == 'Whole_body')]
ratio_whole_body_screen_ls=tmp1['ratio_eyes_on_screen_and_lipsmacking'].mean()
print('Whole_body screen ' +  str(ratio_whole_body_screen_ls))

tmp1 = df_lipsmacking[(df_lipsmacking.category4 == 'face')]
ratio_face_screen_ls=tmp1['ratio_eyes_on_screen_and_lipsmacking'].mean()
print('Face ' +  str(ratio_face_screen_ls))

tmp1 = df_lipsmacking[(df_lipsmacking.category4 == 'noface')]
ratio_noface_screen_ls=tmp1['ratio_eyes_on_screen_and_lipsmacking'].mean()
print('Noface ' +  str(ratio_noface_screen_ls))


print(df_lipsmacking[['MediaName','body_d','lipsmacking_d','looking_at_body_d','category1' ,'ratio_not_eyes_on_screen_and_lipsmacking','ratio_eyes_on_screen_and_lipsmacking']])


#animal, not looking at face
#tmp1 = df_lipsmacking[(df_lipsmacking.animal_ID == 'M3') & (df_lipsmacking.not_looking_at_face_d > 0)]

#animal, not looking at face, lipsmacking
#not_look_face_ls = tmp1[tmp1.lipsmacking_d > 0]

#r2=not_look_face_ls/tmp1



#for i in range(1,a+1):
    

#            if(mctr==1):
#                break
#                        
        
