# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 13:19:35 2022

@author: cacru
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn as sk

games = pd.read_csv("C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2019_games.csv")
pitches = pd.read_csv('C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2019_pitches.csv')
players = pd.read_csv("C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/player_names.csv")
pitcherstats18 = pd.read_csv("C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2018pitchers.csv")
atbats = pd.read_csv('C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2019_atbats.csv')

### This is for the overall 2015 to 2018
# gamesdf = pd.read_csv('C:\\Users\\cacru\\Downloads\\archive\\games.csv')
# pitchesdf = pd.read_csv('C:\\Users\\cacru\\Downloads\\archive\\pitches.csv')
# atbatsdf = pd.read_csv('C:\\Users\\cacru\\Downloads\\archive\\atbats.csv')
# umpire = gamesdf.umpire_HP.unique()
#%%
### Create a strike zone graph based on game stats
### Reference variables in pandas query by utilizing '@'
### game_id in general will follow the format of YEAR#####.0, so 201800001.0 is the first game of 2018
gameid = 201900016.0
### This gives the information for the title
gameinfo = games.query('g_id == @gameid')
hteam = gameinfo['home_team'].values.tolist()
hteam = hteam[0]
ateam = gameinfo['away_team'].values.tolist()
ateam = ateam[0]
gamedate = gameinfo['date'].values.tolist()
gamedate = gamedate[0]
hscore = gameinfo['home_final_score'].values.tolist()
hscore = int(hscore[0])
ascore = gameinfo['away_final_score'].values.tolist()
ascore = int(ascore[0])

gameiddf = atbats.query('g_id == @gameid')
### Merges the two dataframes based on ab_id from pitches. Absolutely amazing
abtest = pd.merge(pitches, gameiddf, how='inner', on='ab_id')
### Use the next line to create graphs based on certain outcomes. I'll list some of the codes below:
'''
code:
X = in play(outs)
B = Ball
D = in play(no outs)
E = in play(runs)
S = Swinging Strike
C = Called Strikes
'''
### You can also sort by the type of pitch thrown. Again, i'll list out the codes below:
'''
pitch_type:
CH - Changeup
CU - Curveball
EP - Eephus*
FC - Cutter
FF - Four-seam Fastball
FO - Pitchout (also PO)*
FS - Splitter
FT - Two-seam Fastball
IN - Intentional ball
KC - Knuckle curve
KN - Knuckeball
PO - Pitchout (also FO)*
SC - Screwball*
SI - Sinker
SL - Slider
We can clean some of the data up if we do not want to include any pitches that may not be worth adding
Things like an eephus, pitchout, intentional ball, and the second pitchout.
'''
abtest = abtest[abtest['code']=='B']
fig, ax = plt.subplots()
ax.axhline(1.5,color='grey',linewidth=1.5)
ax.axhline(3.5,color='grey',linewidth=1.5)
ax.axvline(-0.75, color='grey', linewidth=1.5)
ax.axvline(0.75, color='grey', linewidth=1.5)
ax.axvline(0.25,ymin=0.3,ymax=0.7,color='grey')
ax.axvline(-0.25, ymin=0.3, ymax=0.7, color='grey')
ax.axhline(2.1666, xmin=0.31, xmax=0.69, color='grey')
ax.axhline(2.8333, xmin=0.31, xmax=0.69, color='grey')
ax.axhspan(1.5,3.5,0.31,0.69,color='c',alpha=0.5)
plt.scatter(abtest['px'], abtest['pz'], marker=None, color='black')
plt.xlabel('Pitch X Position in Ft')
plt.ylabel('Pitch Y Position in Ft')
plt.ylim(0,5)
plt.xlim(-2,2)
ax.set_title((f'{gamedate} \n {ateam} at {hteam} \nScore: {ascore} - {hscore}'))
plt.show()

### An idea, calculate the percentage of a pitchers pitches that were on the outer half of the plate,
### cross that with the pitch velocity, pitch break
#%%
pitcherstats18.drop(['Name-additional', 'SV', 'IBB', 'BK', 'WP'], axis=1, inplace=True)
#%%
### Splittting the name in the stats file to make it easier to match up with the players dataframe
### Honestly might be easier to do this the other way around, merging first and last into a single 
### Column for the players file to match the single column in the stats
pstats18 = pitcherstats18
pstats18[['First', 'Last', 'drop1', 'drop2']] = pstats18.Name.str.split(expand=True)
pstats18.drop(['drop1', 'drop2'], axis=1, inplace=True)
pstats18.Last = pstats18.Last.str.strip('*')

### Use pythagorean theroeom to figure out the total distance moved by the pitch.
#%%
### Creating a new dataframe that cleans up the data from some more useless attributes
### When incorporating the 2015 to 2018 data, add spin rate and spin axis
x = pitches[['px','pz','start_speed','end_speed','break_angle',
            'break_length','pitch_type','ab_id',
            'b_count','s_count','outs','pitch_num']
            ].copy()
x.dropna(subset=['px'],inplace=True)
#%%
### Creating a new column that calculates the difference between the start speed and ending speed.
x['speed_dif'] = x['start_speed'] - x['end_speed']
#%%
### Creating a new data frame for pitches in the middle of the strike zone.
middlezone = x.query('px > -0.25 and px < 0.25')
middlezone = middlezone.query('pz > 2.1666 and pz < 2.8333')
x.isnull().sum()
#%%
### Calculating the percentage of pitches over the middle of the zone in the 2019 season.
mid = middlezone.px.count()
ovr = x.px.count()
midpercent = round((mid/ovr)*100, 2)
print('The percentage of pitches over the heart of the zone were:', midpercent,'%')
#%%
