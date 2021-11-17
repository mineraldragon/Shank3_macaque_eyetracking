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
    df['eyes_on_screen'] = (df['GazePointX (ADCSpx)'] > 0) & (df['GazePointY (ADCSpx)'] > 0)
    
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
                if fract>0.5:
                

                
                    mm=m[0:len(m)-4] + ' Recognition'
                    #print(mm)
                    A=df['MediaName'].str.contains(mm)
                    #find rows during which Recognition slide was shown
                    Q_rec=A.index[A == True].tolist()
                    z=list(df)    #all columns
                    #select segment that has the recognition slide
                    df_sel=df.loc[Q_rec]
                    
                    
                    
                    if ('Macaque' in m) or ('Human' in m):
                    
                        if('Macaque' in m):
                            stretch=df.loc[Q_hab,'eyes_on_screen']
                            stretch=stretch.reset_index(drop=True)
                            habdf[m]=stretch
                        
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
                                #print(m)
                                collect[m]=[f1_old, f1_novel]    
                                xs=0;
                            
                    if 'Abstract' in m:
                    
                        print(m)
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
    
str1= 'E:\\Dropbox (MIT)\\Baby macaques\\Preferential Looking Test\\monkey_export_new_old.xlsx'
writer = pd.ExcelWriter(str1)
monkey_new_old.to_excel(writer,'Sheet1')
human_new_old.to_excel(writer,'Sheet2')
abstract_new_old.to_excel(writer,'Sheet3')
writer.save()
writer.close()

m1=monkey[{'C1','C2','C3','C4','CM003','C6'}].mean(axis=0)
m2=monkey[{'M1','M2','M3','M5'}].mean(axis=0)    
str1= 'E:\\Dropbox (MIT)\\Baby macaques\\Preferential Looking Test\\monkey_export.xlsx'
writer = pd.ExcelWriter(str1)
monkey.to_excel(writer,'Sheet1')
writer.save()

plt.figure()
sem1=stats.sem(monkey[{'C1','C2','C3','C4','CM003','C6'}],axis=0)
sem2=stats.sem(monkey[{'M1','M2','M3','M5'}],axis=0)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
#plt.ylim(-0.1, 0.1)
plt.xlim(0.5,2.5)
plt.ylabel('ratio')

h, p=stats.ranksums(monkey[{'C1','C2','C3','C4','CM003','C6'}] , monkey[{'M1','M2','M3','M5'}] )
print(h, p)


m1=human[{'C1','C2','C3','C4','CM003','C6'}].mean(axis=0)
m2=human[{'M1','M2','M3','M5'}].mean(axis=0)    
human.to_excel(writer,'Sheet2')
writer.save()

plt.figure()
sem1=stats.sem(human[{'C1','C2','C3','C4','CM003','C6'}],axis=0)
sem2=stats.sem(human[{'M1','M2','M3','M5'}],axis=0)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
#plt.ylim(-0.1, 0.1)
plt.xlim(0.5,2.5)
plt.ylabel('ratio')

h, p=stats.ranksums(human[{'C1','C2','C3','C4','CM003','C6'}] , human[{'M1','M2','M3','M5'}] )
print(h, p)


m1=abstract[{'C1','C2','C3','C4','CM003','C6'}].mean(axis=0)
m2=abstract[{'M1','M2','M3','M5'}].mean(axis=0)    
abstract.to_excel(writer,'Sheet3')
writer.save()
writer.close()

plt.figure()
sem1=stats.sem(abstract[{'C1','C2','C3','C4','CM003','C6'}],axis=0)
sem2=stats.sem(abstract[{'M1','M2','M3','M5'}],axis=0)
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
plt.xticks([1, 2],['Control','Mutant'])
#plt.ylim(-0.1, 0.1)
plt.xlim(0.5,2.5)
plt.ylabel('ratio')

h, p=stats.ranksums(abstract[{'C1','C2','C3','C4','CM003','C6'}] , abstract[{'M1','M2','M3','M5'}] )
print(h, p)


s3=pd.concat([abstract, human])
s3=pd.concat([s3,monkey])
s3 = s3.reset_index(drop=True)
stimulus=pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
stimulus = stimulus.reset_index(drop=True)
genetics=pd.Series([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0])
genetics = genetics.reset_index(drop=True)
df_res=pd.DataFrame()
df_res['ratio']=s3
df_res['stimulus']=pd.to_numeric(stimulus)
df_res['genetics']=pd.to_numeric(genetics)


m1=MHAB[['C1','C2','C3','C4','CM003','C6']].mean(axis=1)
m2=MHAB[['M1','M2','M3','M5']].mean(axis=1) 
m3=pd.DataFrame()
m3['1']=m1
m3['2']=m2

str1= 'E:\\Dropbox (MIT)\\Baby macaques\\Preferential Looking Test\\monkey_export_traces.xlsx'
writer = pd.ExcelWriter(str1)
m3.to_excel(writer,'Sheet1')
MHAB.to_excel(writer,'Sheet2')
writer.save()
writer.close()

plt.figure()
sem1=stats.sem(MHAB[['C1','C2','C3','C4','CM003','C6']],axis=1)
sem2=stats.sem(MHAB[['M1','M2','M3','M5']],axis=1)
m3.plot()
#plt.errorbar([1:1818],[m1],yerr=[sem1], fmt='o')
#plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
#plt.xticks([1, 2],['Control','Mutant'])
#plt.ylim(-0.1, 0.1)
#plt.xlim(0.5,2.5)
#plt.ylabel('ratio')

#h, p=stats.ranksums(abstract[{'C1','C2','C3','C4','CM003','C6'}] , abstract[{'M1','M2','M3','M5'}] )
#print(h, p)