# Creating a function that allows me to input different things to create different graphs.
# Packages used for the code
#%%
import pandas as pd
import matplotlib.pyplot as plt
#%%
# Getting the data from the CSV files
games = pd.read_csv("C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2019_games.csv")
pitches = pd.read_csv('C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2019_pitches.csv')
players = pd.read_csv("C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/player_names.csv")
pitcherstats18 = pd.read_csv("C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2018pitchers.csv")
atbats = pd.read_csv('C:/Users/Timothy Jordan/Desktop/Pandas Practice/baseball archive/archive/2019_atbats.csv')
#%%
#Defining the function
# Game id format is YEARXXXXX.0
# It needs to be a float
gameid = 201900099.0

def pitchplot(game=0,home=0,away=0, ptype='NA', outcome='NA'):
    # First trying to make the home and away teams lower case to match the format it is in in the data
    # if it can't do this, there will be a specific error given later in the code.
    try:
        home = home.lower()
    except:
        pass
    try:
        away = away.lower()
    except:
        pass
    #List of team names:
    teams = games['home_team'].unique().tolist()
    if game != 0:
        #This section of the if statement gets the information of the specific game if the game id was passed in the function. It includes what teams played, as well as the date and score
        gameinfo = games.query('g_id == @game')
        home_team = gameinfo['home_team'].values.tolist()
        home_team = home_team[0]
        away_team = gameinfo['away_team'].values.tolist()
        away_team = away_team[0]
        game_date = gameinfo['date'].values.tolist()
        game_date = game_date[0]
        home_score = gameinfo['home_final_score'].values.tolist()
        home_score = int(home_score[0])
        away_score = gameinfo['away_final_score'].values.tolist()
        away_score = int(away_score[0])
        gameiddf = atbats.query('g_id == @game')
        
    #This section is checking if the game id was not passed but a home or away team was
    #This would pull the information for the specific teams passed for the entire season.
    elif game == 0:
        if (home not in teams) and (home != 0):
            raise ValueError(f'The input for (home) has to be in the following list:\n{teams}')
        elif (away not in teams) and (away != 0):
            raise ValueError(f'The input for (away) has to be in the following list:\n{teams}')
        elif (home in teams) & (away in teams):
            gameinfo = games[(games['home_team']==home) & (games['away_team']==away)]
            gameids = gameinfo['g_id'].values.tolist()
            gameiddf = atbats[atbats['g_id'].isin(gameids)]
            home_team = home
            away_team = away
            game_date = 'Whole Season'
        elif (home in teams) and (away == 0):
            gameinfo = games[games['home_team']==home]
            gameids = gameinfo['g_id'].values.tolist()
            gameiddf = atbats[atbats['g_id'].isin(gameids)]
            game_date = 'Whole Season'
            team = home
        elif (away in teams) and (home == 0):
            gameinfo = games[games['away_team']==away]
            gameids = gameinfo['g_id'].values.tolist()
            gameiddf = atbats[atbats['g_id'].isin(gameids)]
            game_date = 'Whole Season'
            team = away
            
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
    # Making a list of possible pitch outcomes
    code = ['X', 'B', 'D', 'E', 'S', 'C']
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
    #Making a list of pitch types
    pitch_type = ['CH', 'CU', 'EP', 'FC', 'FF', 'FO',
                  'PO', 'FS', 'FT', 'IN', 'KC', 'KN',
                  'PO', 'FO', 'SC', 'SI', 'SL']
    # Checking if the input for type is a string

    if type(ptype) == str:
        ptype = ptype.upper()
    else:
        raise TypeError('The input for (type) has to be a string')
    # Checking if type has been inputed and in the possible list for pitch types
    if ptype in pitch_type:
        abtest = abtest[abtest['pitch_type'] == ptype]
    elif ptype == 'NA':
        abtest = abtest
    else:
        print(pitch_type)
        raise ValueError(f'The inputed string is not in the list of possible pitch types\nPlease enter a value from the list above\n{pitch_type}')
    
     # Checking if the input for outcome is a string

    if type(outcome) == str:
        outcome = outcome.upper()
    else:
        raise TypeError('The input for (type) has to be a string')
    # Checking if type has been inputed and in the possible list for pitch outcomes
    if outcome in code:
        abtest = abtest[abtest['code'] == outcome]
    elif outcome == 'NA':
        abtest = abtest
    else:
        raise ValueError(f'The inputed string is not in the list of possible pitch outcomes\nPlease enter a value from the list below:\n{code}')
    
    fig, ax = plt.subplots()
    # To figure out how to make the gridlines for the strikezone, I used the avergae height of the strike zone
    # which is 1.5ft to 3.5ft while the plate is 18 inches wide.
    ax.axhline(1.5,color='grey',linewidth=1.5)
    ax.axhline(3.5,color='grey',linewidth=1.5)
    ax.axvline(-0.75, color='grey', linewidth=1.5)
    ax.axvline(0.75, color='grey', linewidth=1.5)
    
    #Creating the outline and fill for the strikezone to make it easier to view
    ax.axvline(0.25,ymin=0.3,ymax=0.7,color='grey')
    ax.axvline(-0.25, ymin=0.3, ymax=0.7, color='grey')
    ax.axhline(2.1666, xmin=0.31, xmax=0.69, color='grey')
    ax.axhline(2.8333, xmin=0.31, xmax=0.69, color='grey')
    ax.axhspan(1.5,3.5,0.31,0.69,color='c',alpha=0.5)
    
    # px is the x cooridinate and pz is the y
    plt.scatter(abtest['px'], abtest['pz'], marker=None, color='black')
    plt.xlabel('Pitch X Position in Ft')
    plt.ylabel('Pitch Y Position in Ft')
    plt.ylim(0,5)
    plt.xlim(-2,2)
    
    #if statement to properly display the information on the table based on what parameters were passed
    if game != 0:
        ax.set_title((f'{game_date} \n {away_team} at {home_team} \nScore: {away_score} - {home_score}'))
    elif (home != 0) and (away != 0):
        ax.set_title((f'{game_date} \n {away_team} at {home_team}'))
    elif (home != 0) and (away == 0):
        ax.set_title((f'{game_date} \n {team} home games'))
    elif (home == 0) and (away != 0):
        ax.set_title((f'{game_date} \n {team} away games'))
    plt.show()
# %%
atbat_id = 2019000002
def filth(id):
    abdf = pitches[pitches['ab_id']==id]
    print(abdf)
filth(atbat_id)
#%%

pitchplot(home='bos',away='min', ptype = 'ff')
# %%
gameiddf = games[games['home_team']=='bos']
gameiddf.keys()
# %%
pitches.keys()
# %%
