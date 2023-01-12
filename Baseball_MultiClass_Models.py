#%%

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %%
games = pd.read_csv("C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2019_games.csv")
pitches = pd.read_csv('C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2019_pitches.csv')
players = pd.read_csv("C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/player_names.csv")
pitcherstats18 = pd.read_csv("C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2018pitchers.csv")
atbats = pd.read_csv('C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2019_atbats.csv')


#%%
# Importing the updated pitches dataframe that has all of the data
pitches2018 = pd.read_csv('C:\\Users\\Timothy Jordan\\Desktop\\Pandas Practice\\baseball archive\\archive\\pitches.csv')

#%%
pitches2018.info()
pitches2018.notnull().count(axis=0)

#%%
# Some preprocessing of the data
# This drops all null values in the pitch_type column which is going to bhe our Y

pitches2018.dropna(subset=['pitch_type'],inplace=True)
# These are pitches that we do not need to consider in our data as they are not normally used in game
dropped_pitches = ['AB', 'UN', 'PO', 'FA', 'EP', 'FO']
pitches2018[pitches2018.pitch_type.isin(dropped_pitches) == False]
# Next, I am going to combine all fastball types into one variable
pitches2018['pitch_type'] = pitches2018['pitch_type'].replace(['FC','FF','FT'], 'FF')
#%%
X = pitches2018.drop(['pitch_type','code','type', 'event_num','ab_id', 'type_confidence', 'px', 'on_1b', 'on_2b',
                      'on_3b', 'pitch_num','zone','outs'], axis=1)
y = pitches2018['pitch_type']

#%%
X.replace([np.inf, -np.inf], np.nan, inplace=True)
from sklearn.impute import SimpleImputer
mean_imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
# Just in case there were any null values since I was getting a Nan, infinity or too large for float64
for item in X.keys():
    mean_imputer = mean_imputer.fit(X[[item]])
    X[item] = mean_imputer.transform(X[[item]])
    
#%%
# Checking if any of the values are infinity
for item in X.keys():
    array = X[item].values.tolist()
    for i in array:
        if np.isinf(i) == True:
            print(item)
            break
        else:
            pass
#%%
print(y.notnull().count())
print(y.count())
# %%
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=100)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
target = ['CH', 'CU', 'EP', 'FC', 'FF', 'FO',
          'PO', 'FS', 'FT', 'IN', 'KC', 'KN',
          'PO', 'FO', 'SC', 'SI', 'SL']
print(classification_report(y_test, y_pred))
# %%
