# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 19:21:11 2022

@author: cacru
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn as sk
import math

### This is for the overall 2015 to 2018
gamesdf = pd.read_csv('C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/games.csv')
pitchesdf = pd.read_csv('C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/pitches.csv')
atbatsdf = pd.read_csv('C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/atbats.csv')
pstats = pd.read_csv('C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2018pitchers.csv')
players = pd.read_csv('C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/player_names.csv')
umpire = gamesdf.umpire_HP.unique()

#%%
### First, create a df that has all the games the umpire managed
### Match that to the ab_ids
### Match that with the pitch_ids
umpirerate = pd.DataFrame(columns=['Name', 'Called Strike Right %', 'Called Ball Right %', 'Average'])
for i in umpire:
    df = gamesdf.query('umpire_HP == @i')
    x = df['g_id']
    df1 = pd.merge(x,atbatsdf,how='inner',on='g_id')
    y = pitchesdf[['px','pz','ab_id', 'code']]
    df1 = pd.merge(y, df1, how='inner',on='ab_id')
    df1 = df1.query('code == "B" | code == "S"')
    s1 = df1.query('px > -0.25 & px < 0.25 & pz > 1.5 & pz < 3.5')
    b1 = df1.query('px < -0.25 | px > 0.25 | pz < 1.5 | pz > 3.5')
    right = s1.query('code == "S"')
    t = s1.px.count()
    r = right.px.count()
    rp = (round((r/t),4))*100
    right1 = b1.query('code == "B"')
    t1 = b1.px.count()
    r1 = right1.px.count()
    rp1 = (round((r1/t1), 4))*100
    avg =(r+r1)/(t+t1)
    temp_lst = [i, rp, rp1, avg]
    temp_df = pd.DataFrame([temp_lst], columns=['Name','Called Strike Right %','Called Ball Right %','Average'])
    umpirerate = umpirerate.append(temp_df)
    
    
#%%
### Writing to Excel file to save the data
umpirerate.to_excel('BaseballInfo.xlsx', sheet_name='Umpire Rates')
#%%
### In this cell, I want to combine the pitcher names with the with their respective stats if they pitched in the 2018 season
### First step is to find out all of the pitchers who pitched in the 2018 season.
step1 = atbatsdf['g_id'].apply(str)
step1a = step1.loc[step1.str.startswith('2018', na=False)]
step1b = step1a.astype(int)
step1c = pd.DataFrame(atbatsdf['pitcher_id'].unique())
step1c = step1c.rename(columns={0:'pitcher_id'})
step1c2 = atbatsdf[atbatsdf['g_id']>2018000000]
step1d = pd.merge(step1c,atbatsdf, how='left', on='pitcher_id' )
step1e = pd.DataFrame(step1d['pitcher_id'].unique())
step1e = step1e.rename(columns={0:'pitcher_id'})
step1f = pd.merge(step1e,players,how='inner', left_on='pitcher_id', right_on='id')
step1f['FullName'] = step1f['first_name']+ ' ' + step1f['last_name']
pstats.Name = pstats.Name.str.strip('*')
pstats.drop(['Name-additional', 'Rk', 'BK', 'WP'], axis=1, inplace=True)
finalstep = pd.merge(step1f, pstats, how='inner', left_on='FullName', right_on='Name')
finalstep.drop(['id', 'Name'], axis=1, inplace=True)
#%%
### Filter to have only pitchers that thrrough at least 20 iunnings
finalstep=finalstep[finalstep.IP > 20]






#%%
totals = finalstep.query('Tm == "TOT"')
for i in finalstep.pitcher_id:
    if i in totals:
        if 
#%%
fig, ax = plt.subplots()
plt.scatter(finalstep['ERA'], finalstep['ERA+'])
plt.xlim(0,10)
plt.ylim(30, 250)
plt.show()
#%%
### Next, we need to calculate the average values for each individual pitch.
### I think we will use a for loop to iterate through each pitch for a certain value
### Step1d from the previous cell can be used in this.
pitches18 = pitchesdf[pitchesdf['ab_id']>2018000000]
fastballmetrics = pd.DataFrame(columns=['pitcher_id', 'avg_velocity','avg_spinrate', 'break_angle', 'breakx', 'breaky','nasty', 'FF_Count', 'FT_Count', 'FC_Count'])
for i in finalstep['pitcher_id']:
    step2 = step1d.query('pitcher_id == @i')
    emptylst = []
    for i in step2['ab_id']:
        df = pitches18[pitches18['ab_id'] == i]
        emptylst.append(df)
    emptydf = pd.concat(emptylst)
    
    ffdf = emptydf[(emptydf['pitch_type']=='FF') | (emptydf['pitch_type'] == 'FT') | (emptydf['pitch_type'] == 'FC')]
    velavg = ffdf.start_speed.mean()
    spinr = ffdf.spin_rate.mean()
    spind = ffdf.break_angle.mean()
    breakx = ffdf.break_length.mean()
    breaky = ffdf.break_y.mean()
    nasty = ffdf.nasty.mean()
    FF = ffdf['pitch_type'].value_counts()['FF']
    FT = ffdf['pitch_type'].value_counts()['FT']
    FC = ffdf['pitch_type'].value_counts()['FC']
    lst2 = [i,velavg,spinr,spind,breakx,breaky,nasty,FF,FT,FC]
    fastballmetrics = pd.concat(lst2)
### Need to compute for individual pitches as the spin rate of a changeup is going to be different than
#%%
'''
Adding average nasty rating
I can reuse this to get the averages on the other stats
'''
pitches18 = pitchesdf[pitchesdf['ab_id']>2018000000]
nasty = pd.DataFrame(columns=['pitcher_id', 'nasty_mean'])
for i in finalstep['pitcher_id']:
    step2 = step1d.query('pitcher_id == @i')
    emptylst = []
    for item in step2['ab_id']:
        df = pitches18[pitches18['ab_id'] == item]
        emptylst.append(df)
    emptydf = pd.concat(emptylst)
    mean = emptydf['nasty'].mean()
    df1 = pd.DataFrame([[i, mean]], columns=['pitcher_id', 'nasty_mean'])
    nasty = nasty.append(df1)
#%%
# lst = [[10, mean]]
# df1 = pd.DataFrame(lst, columns=['pitcher_id', 'nasty_mean'])
# nasty = nasty.append(df1)
finalstep = pd.merge(finalstep, nasty, how='inner', on='pitcher_id')
fig, ax = plt.subplots()
plt.scatter(finalstep['nasty_mean'], finalstep['ERA+'])
