# coding: utf-8

# In[17]:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import math
from scipy import stats

# In[1]:
IDS=['C1', 'C2', 'C3', 'C4','C6', 'M1', 'M2', 'M3', 'M4', 'M5','CM003']
#IDS=['C1']

monkey=pd.Series()
human=pd.Series()
abstract=pd.Series()

monkey_new_old=pd.DataFrame()
human_new_old=pd.DataFrame()
abstract_new_old=pd.DataFrame()

habdf=pd.DataFrame()
MHAB=pd.DataFrame()
supercollect=pd.DataFrame()
for ID in IDS:

    nm='E:\\Dropbox (MIT)\\Baby macaques\\Preferential Looking Test\\pref_looking_' + ID + '.tsv'
    #nm='E:\\Dropbox (MIT)\\Baby macaques\\Preferential Looking Test\\Subset_C1.csv'
    df = pd.read_csv(nm,sep='\t') #read tsv into dataframe
    #df = pd.read_csv(nm) #read tsv into dataframe
    
    #If there is a value, that means the eyes are at the screen
    df['eyes_on_screen'] = (df['GazePointX (ADCSpx)'] > 0) & (df['GazePointX (ADCSpx)'] < 1920) & (df['GazePointY (ADCSpx)'] > 0) & (df['GazePointY (ADCSpx)'] < 1080)
    
    #%%
    A=pd.DataFrame()
    B=pd.DataFrame()
    C=pd.DataFrame()
    q=df.MediaName.unique()      
    collect=pd.DataFrame(index=['old','novel'],columns=q)
    df.MediaName.fillna('0',inplace=True)
    strt=0
    stp=0
    #for each slide..
    for m in q:
        xs=0;    
        if(pd.notnull(m)):
            if 'Recognition' not in m:
                #print(m)
                A=df['MediaName'].str.contains(m)   
                Q_hab=A.index[A == True].tolist()
                #(df['eyes_on_screen']==1).sum()
                length_slide=len(Q_hab)
                length_EOS=df.loc[Q_hab,'eyes_on_screen'].sum()
                fract=length_EOS/length_slide
                #print('fract watched', fract)
                stretch=df.loc[Q_hab,'eyes_on_screen']
                stretch=stretch.reset_index(drop=True)
                habdf[m]=stretch                              
                if fract>0.4:
        
                    mm=m[0:len(m)-4] + ' Recognition'
                    #print(mm)
                    A=df['MediaName'].str.contains(mm)
                    #find rows during which Recognition slide was shown
                    Q_rec=A.index[A == True].tolist()
                    z=list(df)    #all columns
                    #select segment that has the recognition slide
                    df_sel=df.loc[Q_rec]
                    
                    if ('Macaque' in m) or ('Human' in m):
                        
                        #for each column..
                        for c in z:
                            if 'AOI' in c and 'Old' in c and 'Face' in c:
                                #check if any of the rows Q are not null
                                n=df_sel[c]
                                nn=n.notnull().values.any()
                
                                if(nn):
                                    #print(c)
                                    #count 1's and 0's in column c
                                    ones_zeros=n.value_counts()
                                    #print(ones_zeros)
                
                                    if 1.0 in ones_zeros.index:
                                        f1_old=ones_zeros[1.0]
                                    else:
                                        f1_old=0
                                    xs=xs+1;  
                                    
                            if 'AOI' in c and 'Novel' in c and 'Face' in c:
                                #check if any of the rows Q are not null
                                n=df_sel[c]
                                nn=n.notnull().values.any()
                                #print(nn)
                                if(nn):
                                    #print(c)
                                    #count 1's and 0's in column c
                                    ones_zeros=n.value_counts()
                                    #print(ones_zeros)
                
                                    if 1.0 in ones_zeros.index:
                                        f1_novel=ones_zeros[1.0]
                                    else:
                                        f1_novel=0
                                    xs=xs+1;    
                                          
                            if(xs==2):    
                                print(m)
                                #print(ones_zeros)
                                print(f1_old)
                                print(f1_novel)
                                if(f1_old>0 | f1_novel>0):
                                    collect[m]=[f1_old, f1_novel]    
                                xs=0;
                            
                    if 'Abstract' in m:
                    
                        #print(m)
                        #for each column..
                        for c in z:
                            if 'AOI' in c and 'Old' in c and 'Abstract' in c:
                                #check if any of the rows Q are not null
                                n=df_sel[c]
                                nn=n.notnull().values.any()
                
                                if(nn):
                                    #print(c)
                                    #count 1's and 0's in column c
                                    ones_zeros=n.value_counts()
                                    #print(ones_zeros)
                
                                    if 1.0 in ones_zeros.index:
                                        f1_old=ones_zeros[1.0]
                                    else:
                                        f1_old=0
                                    xs=xs+1;  
                                    
                            if 'AOI' in c and 'Novel' in c and 'Abstract' in c:
                                #check if any of the rows Q are not null
                                n=df_sel[c]
                                nn=n.notnull().values.any()
                                #print(nn)
                                if(nn):
                                    #print(c)
                                    #count 1's and 0's in column c
                                    ones_zeros=n.value_counts()
                                    #print(ones_zeros)
                
                                    if 1.0 in ones_zeros.index:
                                        f1_novel=ones_zeros[1.0]
                                    else:
                                        f1_novel=0
                                    xs=xs+1;    
                                          
                            if(xs==2):    
                                #print(m)
                                collect[m]=[f1_old, f1_novel]    
                                xs=0;    
    
    
    mhab=habdf.mean(axis=1)
    MHAB[ID]=mhab
    
    collect['ID']=ID
    print(ID)
    df2 = collect.filter(regex='Macaque')
    mm=df2.mean(axis=1)
    print(mm)
    #monkey[ID]=(mm['novel']-mm['old'])/(mm['novel']+mm['old'])
    monkey[ID]=mm['novel']/mm['old']
    
    if(ID=='C1'):
        monkey_new_old=pd.DataFrame(mm).transpose()
    else:
        tmp=pd.DataFrame(mm).transpose()
        frames=[monkey_new_old,tmp]
        monkey_new_old = pd.concat(frames)
        
    
    df2 = collect.filter(regex='Human')
    mm=df2.mean(axis=1)
    print(mm)
    #human[ID]=(mm['novel']-mm['old'])/(mm['novel']+mm['old'])
    human[ID]=mm['novel']/mm['old']
    
    if(ID=='C1'):
        human_new_old=pd.DataFrame(mm).transpose()
    else:
        tmp=pd.DataFrame(mm).transpose()
        frames=[human_new_old,tmp]
        human_new_old = pd.concat(frames)    
    
    
    df2 = collect.filter(regex='Abstract')
    mm=df2.mean(axis=1)
    print(mm)
    #abstract[ID]=(mm['novel']-mm['old'])/(mm['novel']+mm['old'])
    abstract[ID]=mm['novel']/mm['old']
    
    if(ID=='C1'):
        abstract_new_old=pd.DataFrame(mm).transpose()
    else:
        tmp=pd.DataFrame(mm).transpose()
        frames=[abstract_new_old,tmp]
        abstract_new_old = pd.concat(frames)
    
    if(ID=='C1'):
        supercollect=collect
    else:
        supercollect=pd.concat([supercollect, collect])
    
