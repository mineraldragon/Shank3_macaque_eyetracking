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
habdf_bars=pd.DataFrame(columns=['1','2','3','rec'])

MHAB=pd.DataFrame()
MHAB_exp=pd.DataFrame()
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
            if ('Recognition' not in m) & ('breakslide' not in m):
                
                print(m)
                A=df['MediaName'].str.contains(m)  
                mm=m[0:len(m)-4] + ' Recognition'
                Arec=df['MediaName'].str.contains(mm)
                
                Bstr= (df['StudioEventData'].str.contains(m) & df['StudioEvent'].str.contains('Start'))
                Bstp= (df['StudioEventData'].str.contains(m) & df['StudioEvent'].str.contains('End'))
                
                Bstr_rec= (df['StudioEventData'].str.contains(mm) & df['StudioEvent'].str.contains('Start'))
                Bstp_rec= (df['StudioEventData'].str.contains(mm) & df['StudioEvent'].str.contains('End'))                
                
                B_hab1=Bstr.index[Bstr == True].tolist()
                B_hab2=Bstr.index[Bstp == True].tolist()

                B_hab1_rec=Bstr_rec.index[Bstr_rec == True].tolist()
                B_hab2_rec=Bstr_rec.index[Bstp_rec == True].tolist()
                
                #B_hab=A.index[A == True].tolist()
                print(B_hab1)
                print(B_hab2)

                print(B_hab1_rec)
                print(B_hab2_rec)
                
                exp1_list=list(range(B_hab1[0],B_hab2[0]))
                exp2_list=list(range(B_hab1[1],B_hab2[1]))
                exp3_list=list(range(B_hab1[2],B_hab2[2]))
                if len(B_hab1_rec) & len(B_hab2_rec):
                    exp_rec_list=list(range(B_hab1_rec[0],B_hab2_rec[0]))
                
                length_exp1=len(exp1_list)
                length_exp2=len(exp2_list)
                length_exp3=len(exp3_list)
                if len(B_hab1_rec) & len(B_hab2_rec):
                    length_exp_rec=len(exp_rec_list)
                
                length_EOS1=df.loc[exp1_list,'eyes_on_screen'].sum()
                length_EOS2=df.loc[exp2_list,'eyes_on_screen'].sum()
                length_EOS3=df.loc[exp3_list,'eyes_on_screen'].sum()
                if len(B_hab1_rec) & len(B_hab2_rec):
                    length_EOS_rec=df.loc[exp_rec_list,'eyes_on_screen'].sum()
                
                if len(B_hab1_rec) & len(B_hab2_rec):
                    habdf_bars.loc[m] = pd.Series({'1':length_EOS1/length_exp1, '2':length_EOS2/length_exp2, '3':length_EOS3/length_exp3, 'rec':length_EOS_rec/length_exp_rec })
                else:
                    habdf_bars.loc[m] = pd.Series({'1':length_EOS1/length_exp1, '2':length_EOS2/length_exp2, '3':length_EOS3/length_exp3, 'rec':np.nan })
                    
#                stretch=df.loc[exp1_list,'eyes_on_screen']
#                stretch=stretch.reset_index(drop=True)
#                habdf1[m]=stretch 
#                
#                stretch=df.loc[exp1_list,'eyes_on_screen']
#                stretch=stretch.reset_index(drop=True)
#                habdf1[m]=stretch 

                
                #print(Bstp)
                Q_hab=A.index[A == True].tolist()
                #(df['eyes_on_screen']==1).sum()
                length_slide=len(Q_hab)
                length_each=round(length_slide/3);
                
                length_EOS=df.loc[Q_hab,'eyes_on_screen'].sum()

                fract=length_EOS/length_slide
                #print('fract watched', fract)

                stretch=df.loc[Q_hab,'eyes_on_screen']
                stretch=stretch.reset_index(drop=True)
                habdf[m]=stretch  
                            
                if fract>0.5:
                

                
                    mm=m[0:len(m)-4] + ' Recognition'
                    #print(mm)
                    A=df['MediaName'].str.contains(mm)
                    #find rows during which Recognition slide was shown
                    Q_rec=A.index[A == True].tolist()
                    z=list(df)    #all columns
                    #select segment that has the recognition slide
                    df_sel=df.loc[Q_rec]
                    
                        #if('Macaque' in m):
                  
                    
                    if ('Macaque' in m) or ('Human' in m):
                    
#                        if('Macaque' in m):
#                            stretch=df.loc[Q_hab,'eyes_on_screen']
#                            stretch=stretch.reset_index(drop=True)
#                            habdf[m]=stretch
                        
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
    habdf_bars=habdf_bars.replace([np.inf, -np.inf], np.nan)
    mhab_exp=habdf_bars.mean(axis=0)
    mhab_exp=mhab_exp.T #transpose
    MHAB[ID]=mhab
    MHAB_exp[ID]=mhab_exp
    
    collect['ID']=ID
    print(ID)
    df2 = collect.filter(regex='Macaque')
    mm=df2.mean(axis=1)
    print(mm)
    monkey[ID]=(mm['novel']-mm['old'])/(mm['novel']+mm['old'])
    #monkey[ID]=mm['novel']/mm['old']
    
    if(ID=='C1'):
        monkey_new_old=pd.DataFrame(mm).transpose()
    else:
        tmp=pd.DataFrame(mm).transpose()
        frames=[monkey_new_old,tmp]
        monkey_new_old = pd.concat(frames)
        
    
    df2 = collect.filter(regex='Human')
    mm=df2.mean(axis=1)
    print(mm)
    human[ID]=(mm['novel']-mm['old'])/(mm['novel']+mm['old'])
    #human[ID]=mm['novel']/mm['old']
    
    if(ID=='C1'):
        human_new_old=pd.DataFrame(mm).transpose()
    else:
        tmp=pd.DataFrame(mm).transpose()
        frames=[human_new_old,tmp]
        human_new_old = pd.concat(frames)    
    
    
    df2 = collect.filter(regex='Abstract')
    mm=df2.mean(axis=1)
    print(mm)
    abstract[ID]=(mm['novel']-mm['old'])/(mm['novel']+mm['old'])
    #abstract[ID]=mm['novel']/mm['old']
    
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
writer = pd.ExcelWriter(str1, engine='xlsxwriter')
monkey_new_old.to_excel(writer,'Sheet1')
human_new_old.to_excel(writer,'Sheet2')
abstract_new_old.to_excel(writer,'Sheet3')
writer.save()
writer.close()

m1=monkey[{'C1','C2','C3','C4','CM003','C6'}].mean(axis=0)
m2=monkey[{'M1','M2','M3','M5'}].mean(axis=0)    
str1= 'E:\\Dropbox (MIT)\\Baby macaques\\Preferential Looking Test\\monkey_export.xlsx'
writer = pd.ExcelWriter(str1, engine='xlsxwriter')
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
writer = pd.ExcelWriter(str1, engine='xlsxwriter')
m3.to_excel(writer,'Sheet1')
MHAB.to_excel(writer,'Sheet2')
writer.save()
writer.close()

plt.figure()
sem1=stats.sem(MHAB[['C1','C2','C3','C4','CM003','C6']],axis=1)
sem2=stats.sem(MHAB[['M1','M2','M3','M5']],axis=1)
m3.plot()


str1= 'E:\\Dropbox (MIT)\\Baby macaques\\Preferential Looking Test\\monkey_export_hab.xlsx'
writer = pd.ExcelWriter(str1, engine='xlsxwriter')
MHAB_exp.to_excel(writer,'Sheet1')
writer.save()
writer.close()

#plt.figure()
#sem1=stats.sem(MHAB_exp[{'C1','C2','C3','C4','CM003','C6'}],axis=0)
#sem2=stats.sem(MHAB_exp[{'M1','M2','M3','M5'}],axis=0)
#plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
#plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
#plt.xticks([1, 2],['Control','Mutant'])
##plt.ylim(-0.1, 0.1)
#plt.xlim(0.5,2.5)
#plt.ylabel('ratio')

#plt.errorbar([1:1818],[m1],yerr=[sem1], fmt='o')
#plt.errorbar([1, 2],[m1, m2],yerr=[sem1, sem2], fmt='o')
#plt.xticks([1, 2],['Control','Mutant'])
#plt.ylim(-0.1, 0.1)
#plt.xlim(0.5,2.5)
#plt.ylabel('ratio')

#h, p=stats.ranksums(abstract[{'C1','C2','C3','C4','CM003','C6'}] , abstract[{'M1','M2','M3','M5'}] )
#print(h, p)

