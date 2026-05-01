#q1:
import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df=pd.read_csv("assets/nhl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def nhl_correlation(): 
    # YOUR CODE HERE
    #print(cities.head())
    #print(cities.columns)
    cities_selected = cities[[ 'Metropolitan area', 'NHL','Population (2016 est.)[8]']]
    #print(cities_selected)
    #print all nhl team names 
    #print(cities_selected['NHL'].to_string())
    #clean up NHL team names in cities_selected
    def clean_ct_team_name(pattern):
        replacements = {}
        needs_corr = cities_selected['NHL'].str.contains(pattern, regex=True)
        matching_names = cities_selected.loc[needs_corr, 'NHL']
        for team in list(matching_names):
            team_name = team.split("[")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    cities_selected['NHL'] = cities_selected['NHL'].replace(clean_ct_team_name(r".+note.+"))
    cities_selected['NHL'] = cities_selected['NHL'].replace({"—":""})
    #drop row if column is empty
    cities_selected = cities_selected[cities_selected['NHL'] != '']
    #print(cities_selected[['Metropolitan area','NHL']])
   
    #clean up columns with two or more teams
    #print(cities_selected)   
    #Rangers Islanders Devils is Rangers Islanders and Devils
    #Kings Ducks is Kings & Ducks
    #function to duplicate rows of cities_selected
    def dupl_row(row_index_to_duplicate):
        #row_index_to_duplicate = 0
        # Select the specific row
        row_to_add = cities_selected.iloc[[row_index_to_duplicate]]
        # Concatenate the original DataFrame and the duplicated row(s)
        # ignore_index=True resets the index of the final DataFrame
        duplicated_df = pd.concat([cities_selected, row_to_add], ignore_index=True)
        return duplicated_df
        
    cities_selected = dupl_row(0)
    cities_selected = dupl_row(0)
    cities_selected = dupl_row(1)
    #print(cities_selected.index)
    #Rename the value in column 'NHL' at index '0' to 10
    cities_selected.at[0, 'NHL'] = 'Rangers'
    cities_selected.at[1, 'NHL'] = 'Kings'
    cities_selected.at[28, 'NHL'] = 'Islanders'
    cities_selected.at[29, 'NHL'] = 'Devils'
    cities_selected.at[30, 'NHL'] = 'Ducks'
    #print(cities_selected)
    #print(cities_selected['NHL'].to_string())
       
    
    #print(nhl_df.columns)
    #nhl using 2018 data
    nhl_df_18 = nhl_df.loc[nhl_df['year'] == 2018]
    #print(nhl_df_18.head())
    #print(nhl_df_18['team'].to_string())
    
    #clean up team names remove *
    #team names cleaning, using a function
    def clean_team_name(pattern):
        replacements = {}
        needs_corr = nhl_df_18['team'].str.contains(pattern, regex=True)
        matching_names = nhl_df_18.loc[needs_corr, 'team']
        for team in list(matching_names):
            team_name = team.split("*")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    nhl_df_18['team'] = nhl_df_18['team'].replace(clean_team_name(r"[\w\s]+\*$"))
    #print(nhl_df_18['team'].to_string())
    #drop rows with division 
    df_indexed = nhl_df_18.set_index('team')
    idx_nhl_list = nhl_df_18['team'].tolist()
    #print(df_indexed)
    #print(idx_nhl_list)
    for tm in idx_nhl_list:
        team_name = tm.split(" ")
        if 'Division' in team_name:
            #print(team_name)
            df_indexed.drop([tm], inplace=True)
    
    #print(df_indexed)
    nhl_df_18 = df_indexed.reset_index()
    #print(nhl_df_18)
    
    #create new column with w/l ratio
    nhl_df_18 = nhl_df_18.astype({'W': float, 'L': float})
    nhl_df_18['win/loss ratio'] = (nhl_df_18['W'] / (nhl_df_18['L'] + nhl_df_18['W']))
    #print(nhl_df_18)
    
    
    #Rename the following list of teams in cities_selected
    #function to return dictionary of replacements in cities_selected
    def replacements_dict():
        replacements={}
        cities_nhl_list = cities_selected['NHL'].tolist()
        nhl_teams_list= nhl_df_18['team'].tolist()
        for team in cities_nhl_list:
            for nhl_team in nhl_teams_list:
                team_name = nhl_team.split(" ")
                if team in team_name:
                    replacements[team]=nhl_team
        return replacements 
            
    #print(replacements_dict())        
    #replacements = {'Rangers': 'New York Rangers', 'Kings': 'Los Angeles Kings', 'Sharks':'San Jose Sharks', 'Blackhawks': 'Chicago Blackhawks', 'Stars':'Dallas Stars', 
    #                'Capitals':'Washington Capitals', 'Flyers':'Philadelphia Flyers'}
    cities_selected['NHL'] = cities_selected['NHL'].replace(replacements_dict())
    #print(cities_selected)
    
    #For regions with multiple teams in them such as New York and Los Angeles, you should average out the win loss ratios of individual teams 
    #in those regions
    #drop Anaheim Ducks, New Jersey Devils,  New York Islanders
    cities_selected.drop([28, 29, 30], inplace=True) #keep only new york rangers and los angeles kings
    #print(cities_selected)
    #print(nhl_df_18)   
    nhl_df_18.iat[26, 15] = 0.5 *(nhl_df_18.iat[26, 15] + nhl_df_18.iat[24, 15])
    nhl_df_18.iat[15, 15] = 0.333 *(nhl_df_18.iat[15, 15] + nhl_df_18.iat[14, 15] + nhl_df_18.iat[12, 15] )
    nhl_df_18.drop([24, 14, 12], inplace=True)
    #print(nhl_df_18)
      
    #sort according to teams name both cities_selected and nhl_df_18
    #print(cities_selected)
    cities_selected['NHL'] = cities_selected['NHL'].replace({'Blue Jackets': 'Columbus Blue Jackets', 'Maple Leafs' : 'Toronto Maple Leafs', 
                                                             'Red Wings':'Detroit Red Wings', 'Golden Knights':'Vegas Golden Knights'})
    cities_selected = cities_selected.astype({'Population (2016 est.)[8]': int})
    
    nhl_df_18.sort_values(by='team', inplace=True)
    cities_selected.sort_values(by='NHL', inplace=True)    
    nhl_df_18 = nhl_df_18.reset_index()
    cities_selected = cities_selected.reset_index()
    nhl_df_18 = nhl_df_18.drop('index', axis=1)
    cities_selected = cities_selected.drop('index', axis=1)
    #print(cities_selected)
    #print(nhl_df_18)
    
    #print(nhl_df_18[['win/loss ratio', 'team']])
    #print(cities_selected[['Population (2016 est.)[8]', 'NHL']])
    #raise NotImplementedError()
    #print(len(nhl_df_18['win/loss ratio'].to_list()))
    #print(len(cities_selected['Population (2016 est.)[8]'].to_list()))
    population_by_region = cities_selected['Population (2016 est.)[8]'].to_list() # pass in metropolitan area population from cities
    win_loss_by_region = nhl_df_18['win/loss ratio'].to_list() # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"   
    corr, p_value = stats.pearsonr(population_by_region, win_loss_by_region)
    return corr 
    #return 0
    
#print(nhl_correlation())

#q2:

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nba_df=pd.read_csv("assets/nba.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def nba_correlation():
    # YOUR CODE HERE
    #print(cities.head())
    #print(cities.columns)
    cities_selected = cities[[ 'Metropolitan area', 'NBA','Population (2016 est.)[8]']]
    #print(cities_selected)
   
    #clean up NBA team names in cities_selected, remove [note]
    def clean_ct_team_name(pattern):
        replacements = {}
        needs_corr = cities_selected['NBA'].str.contains(pattern, regex=True)
        matching_names = cities_selected.loc[needs_corr, 'NBA']
        for team in list(matching_names):
            team_name = team.split("[")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    cities_selected['NBA'] = cities_selected['NBA'].replace(clean_ct_team_name(r".+note.+"))
    cities_selected['NBA'] = cities_selected['NBA'].replace({"—":""})
    #drop row if column is empty
    cities_selected = cities_selected[cities_selected['NBA'] != '']
    #print(cities_selected)
     
    
    #function to duplicate rows of cities_selected
    def dupl_row(row_index_to_duplicate):
        #row_index_to_duplicate = 0
        # Select the specific row
        row_to_add = cities_selected.iloc[[row_index_to_duplicate]]
        # Concatenate the original DataFrame and the duplicated row(s)
        # ignore_index=True resets the index of the final DataFrame
        duplicated_df = pd.concat([cities_selected, row_to_add], ignore_index=True)
        return duplicated_df
        
    cities_selected = dupl_row(0)
    cities_selected = dupl_row(1)
    
    #print(cities_selected)
    #Rename the value in column 'NBA' at index '0' to 10
    cities_selected.at[0, 'NBA'] = 'Knicks'
    cities_selected.at[1, 'NBA'] = 'Lakers'
    cities_selected.at[28, 'NBA'] = 'Nets'
    cities_selected.at[29, 'NBA'] = 'Clippers'
    
    #print(cities_selected)   
    
    #NBA using 2018 data
    nba_df_18 = nba_df.loc[nba_df['year'] == 2018]
    #print(nba_df_18)
    
    #clean up team names remove * and number
    #team names cleaning, using a function
    def clean_team_name(pattern):
        replacements = {}
        needs_corr = nba_df_18['team'].str.contains(pattern, regex=True)
        matching_names = nba_df_18.loc[needs_corr, 'team']
        for team in list(matching_names):
            team_name = team.split("*")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    nba_df_18['team'] = nba_df_18['team'].replace(clean_team_name(r"[\w\s]+[\*].*"))
    #print(nba_df_18)
    
     #clean up team names remove ( and number
    #team names cleaning, using a function
    def clean_team_name(pattern):
        replacements = {}
        needs_corr = nba_df_18['team'].str.contains(pattern, regex=True)
        matching_names = nba_df_18.loc[needs_corr, 'team']
        for team in list(matching_names):
            team_name = team.split("(")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    nba_df_18['team'] = nba_df_18['team'].replace(clean_team_name(r"[\w\s]+[\(].*"))
    #print(nba_df_18)
    
     #Rename the following list of teams in cities_selected
    #function to return dictionary of replacements in cities_selected
    def replacements_dict():
        replacements={}
        cities_nba_list = cities_selected['NBA'].tolist()
        nba_teams_list= nba_df_18['team'].tolist()
        for team in cities_nba_list:
            for nba_team in nba_teams_list:
                team_name = nba_team.split(" ")
                team_name[-1]=team_name[-1].replace('\xa0', '')
                #print(team_name, team)
                if team in team_name:
                    replacements[team]=nba_team
        return replacements 
            
    #print(replacements_dict())        
    cities_selected['NBA'] = cities_selected['NBA'].replace(replacements_dict())
    cities_selected['NBA'] = cities_selected['NBA'].replace({'Trail Blazers':'Portland Trail Blazers'})
    #print(cities_selected)
     
     #For regions with multiple teams in them you should average out the win loss ratios of individual teams 
    #in those regions
    #drop Los Angeles Clippers,Brooklyn Nets
    cities_selected.drop([28, 29], inplace=True) 
    #print(cities_selected)
    #print(nba_df_18.iat[24, 3], nba_df_18.iat[25, 3])
    #print(nba_df_18)
    nba_df_18 = nba_df_18.astype({'W/L%': float})
    nba_df_18.iat[25, 3] = 0.5 *(nba_df_18.iat[24, 3] + nba_df_18.iat[25, 3])
    nba_df_18.iat[10, 3] = 0.5 *(nba_df_18.iat[10, 3] + nba_df_18.iat[11, 3])
    nba_df_18.drop([24, 11], inplace=True)
    #print(nba_df_18)
     
    
    cities_selected = cities_selected.astype({'Population (2016 est.)[8]': int})
    
    nba_df_18.sort_values(by='team', inplace=True)
    cities_selected.sort_values(by='NBA', inplace=True)    
    nba_df_18 = nba_df_18.reset_index()
    cities_selected = cities_selected.reset_index()
    nba_df_18 = nba_df_18.drop('index', axis=1)
    cities_selected = cities_selected.drop('index', axis=1)
    #print(cities_selected)
    #print(nba_df_18)
     
    #raise NotImplementedError()
    
    population_by_region = cities_selected['Population (2016 est.)[8]'].to_list() # pass in metropolitan area population from cities
    win_loss_by_region = nba_df_18['W/L%'].to_list() # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"
    corr, p_value = stats.pearsonr(population_by_region, win_loss_by_region)
    return corr
    #return 0

#print(nba_correlation())

#q3:

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def mlb_correlation(): 
    # YOUR CODE HERE
    cities_selected = cities[[ 'Metropolitan area', 'MLB','Population (2016 est.)[8]']]
    #print(cities_selected)
   
    #clean up NBA team names in cities_selected, remove [note]
    def clean_ct_team_name(pattern):
        replacements = {}
        needs_corr = cities_selected['MLB'].str.contains(pattern, regex=True)
        matching_names = cities_selected.loc[needs_corr, 'MLB']
        for team in list(matching_names):
            team_name = team.split("[")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    cities_selected['MLB'] = cities_selected['MLB'].replace(clean_ct_team_name(r".+note.+"))
    cities_selected['MLB'] = cities_selected['MLB'].replace({"—":""})
    #drop row if column is empty
    cities_selected = cities_selected[cities_selected['MLB'] != '']
    #print(cities_selected)
    
    #function to duplicate rows of cities_selected
    def dupl_row(row_index_to_duplicate):
        #row_index_to_duplicate = 0
        # Select the specific row
        row_to_add = cities_selected.iloc[[row_index_to_duplicate]]
        # Concatenate the original DataFrame and the duplicated row(s)
        # ignore_index=True resets the index of the final DataFrame
        duplicated_df = pd.concat([cities_selected, row_to_add], ignore_index=True)
        return duplicated_df
        
    cities_selected = dupl_row(0)
    cities_selected = dupl_row(1)
    cities_selected = dupl_row(2)
    cities_selected = dupl_row(3)
    
    #print(cities_selected)
    #Rename the value in column 'NBA' at index '0' to 10
    cities_selected.at[0, 'MLB'] = 'Yankees'
    cities_selected.at[1, 'MLB'] = 'Dodgers'
    cities_selected.at[2, 'MLB'] = 'Giants'
    cities_selected.at[3, 'MLB'] = 'Cubs'
    
    cities_selected.at[26, 'MLB'] = 'Mets'
    cities_selected.at[27, 'MLB'] = 'Angels'
    cities_selected.at[28, 'MLB'] = 'Athletics'
    cities_selected.at[29, 'MLB'] = 'White Sox'
      
    #print(cities_selected)
    
    #MLB using 2018 data
    mlb_df_18 = mlb_df.loc[mlb_df['year'] == 2018]
    #print(mlb_df_18)
    
    #Rename the following list of teams in cities_selected
    #function to return dictionary of replacements in cities_selected
    def replacements_dict():
        replacements={}
        cities_mlb_list = cities_selected['MLB'].tolist()
        mlb_teams_list= mlb_df_18['team'].tolist()
        for team in cities_mlb_list:
            for mlb_team in mlb_teams_list:
                team_name = mlb_team.split(" ")
                #print(team_name, team) 
                if team.split(" ")[0] in team_name:
                    replacements[team]=mlb_team
        return replacements 
            
    #print(replacements_dict())        
    cities_selected['MLB'] = cities_selected['MLB'].replace(replacements_dict())
    #print(cities_selected)    
    #print(mlb_df_18)
    
    #For regions with multiple teams in them you should average out the win loss ratios of individual teams 
    #in those regions
    #drop New York Mets, Los Angeles Angels, Oakland Athletics, Chicago White Sox 
    cities_selected.drop([26, 27, 28, 29], inplace=True) 
    #print(cities_selected)
    #print(mlb_df_18.iat[24, 3], mlb_df_18.iat[25, 3])
    #print(mlb_df_18)
    mlb_df_18 = mlb_df_18.astype({'W-L%': float})
    mlb_df_18.iat[1, 3] = 0.5 *(mlb_df_18.iat[1, 3] + mlb_df_18.iat[18, 3])
    mlb_df_18.iat[25, 3] = 0.5 *(mlb_df_18.iat[25, 3] + mlb_df_18.iat[13, 3])
    mlb_df_18.iat[28, 3] = 0.5 *(mlb_df_18.iat[28, 3] + mlb_df_18.iat[11, 3])
    mlb_df_18.iat[21, 3] = 0.5 *(mlb_df_18.iat[21, 3] + mlb_df_18.iat[8, 3])
    
    mlb_df_18.drop([18, 13, 11, 8], inplace=True)
    #print(mlb_df_18)
    
    cities_selected = cities_selected.astype({'Population (2016 est.)[8]': int})
    
    mlb_df_18.sort_values(by='team', inplace=True)
    cities_selected.sort_values(by='MLB', inplace=True)    
    mlb_df_18 = mlb_df_18.reset_index()
    cities_selected = cities_selected.reset_index()
    mlb_df_18 = mlb_df_18.drop('index', axis=1)
    cities_selected = cities_selected.drop('index', axis=1)
    #print(cities_selected)
    #print(mlb_df_18)
    
    
    
    #raise NotImplementedError()
    population_by_region = cities_selected['Population (2016 est.)[8]'].to_list() # pass in metropolitan area population from cities
    win_loss_by_region = mlb_df_18['W-L%'].to_list() # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    corr, pval=stats.pearsonr(population_by_region, win_loss_by_region)
    return corr
    
#print(mlb_correlation())


#q4:

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def nfl_correlation(): 
    # YOUR CODE HERE
    cities_selected = cities[[ 'Metropolitan area', 'NFL','Population (2016 est.)[8]']]
    #print(cities_selected)
   
    #clean up NBA team names in cities_selected, remove [note]
    def clean_ct_team_name(pattern):
        replacements = {}
        needs_corr = cities_selected['NFL'].str.contains(pattern, regex=True)
        matching_names = cities_selected.loc[needs_corr, 'NFL']
        for team in list(matching_names):
            team_name = team.split("[")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    cities_selected['NFL'] = cities_selected['NFL'].replace(clean_ct_team_name(r".+note.+"))
    cities_selected['NFL'] = cities_selected['NFL'].replace({"—":""})
    cities_selected.drop([13], inplace=True)
    #print(cities_selected.iat[13,1])
    #drop row if column is empty
    cities_selected = cities_selected[cities_selected['NFL'] != '']
    #print(cities_selected)
    
    #function to duplicate rows of cities_selected
    def dupl_row(row_index_to_duplicate):
        #row_index_to_duplicate = 0
        # Select the specific row
        row_to_add = cities_selected.iloc[[row_index_to_duplicate]]
        # Concatenate the original DataFrame and the duplicated row(s)
        # ignore_index=True resets the index of the final DataFrame
        duplicated_df = pd.concat([cities_selected, row_to_add], ignore_index=True)
        return duplicated_df
        
    cities_selected = dupl_row(0)
    cities_selected = dupl_row(1)
    cities_selected = dupl_row(2)
    
    #Rename the value in column 'NBA' at index '0' to 10
    cities_selected.at[0, 'NFL'] = 'Giants'
    cities_selected.at[1, 'NFL'] = 'Rams'
    cities_selected.at[2, 'NFL'] = '49ers'
    
    cities_selected.at[29, 'NFL'] = 'Jets'
    cities_selected.at[30, 'NFL'] = 'Chargers'
    cities_selected.at[31, 'NFL'] = 'Raiders'
    
    #print(cities_selected)  
     
    #MLB using 2018 data
    nfl_df_18 = nfl_df.loc[nfl_df['year'] == 2018]
    #print(nfl_df_18)    
        
    #clean up team names remove * and +
    #team names cleaning, using a function
    def clean_team_name(pattern):
        replacements = {}
        needs_corr = nfl_df_18['team'].str.contains(pattern, regex=True)
        matching_names = nfl_df_18.loc[needs_corr, 'team']
        for team in list(matching_names):
            team_name = team.split("*")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    nfl_df_18['team'] = nfl_df_18['team'].replace(clean_team_name(r"[\w\s]+\*$"))
    
    def clean_team_name(pattern):
        replacements = {}
        needs_corr = nfl_df_18['team'].str.contains(pattern, regex=True)
        matching_names = nfl_df_18.loc[needs_corr, 'team']
        for team in list(matching_names):
            team_name = team.split("+")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    nfl_df_18['team'] = nfl_df_18['team'].replace(clean_team_name(r"[\w\s]+\+$"))
    #print(nfl_df_18)    
    
    #drop rows with AFC or NFC 
    df_indexed = nfl_df_18.set_index('team')
    idx_nfl_list = nfl_df_18['team'].tolist()
    #print(df_indexed)
    #print(idx_nhl_list)
    for tm in idx_nfl_list:
        team_name = tm.split(" ")
        if 'AFC' in team_name or 'NFC' in team_name:
            #print(team_name)
            df_indexed.drop([tm], inplace=True)
    
    #print(df_indexed)
    nfl_df_18 = df_indexed.reset_index()
    #print(nfl_df_18)
    
    #Rename the following list of teams in cities_selected
    #function to return dictionary of replacements in cities_selected
    def replacements_dict():
        replacements={}
        cities_nfl_list = cities_selected['NFL'].tolist()
        nfl_teams_list= nfl_df_18['team'].tolist()
        for team in cities_nfl_list:
            for nfl_team in nfl_teams_list:
                team_name = nfl_team.split(" ")
                #print(team_name, team) 
                if team.split(" ")[0] in team_name:
                    replacements[team]=nfl_team
        return replacements 
            
    #print(replacements_dict())        
    cities_selected['NFL'] = cities_selected['NFL'].replace(replacements_dict())
    #print(cities_selected)    
    #print(nfl_df_18)
    
     #For regions with multiple teams in them you should average out the win loss ratios of individual teams 
    #in those regions
    #drop New York Jets, Los Angeles Chargers, Oakland Raiders 
    cities_selected.drop([29, 30, 31], inplace=True) 
    #print(cities_selected)
    #print(nfl_df_18.iat[24, 13], nfl_df_18.iat[25, 13])
    #print(nfl_df_18)
    nfl_df_18 = nfl_df_18.astype({'W-L%': float})
    nfl_df_18.iat[19, 13] = 0.5 *(nfl_df_18.iat[19, 13] + nfl_df_18.iat[3, 13])
    nfl_df_18.iat[28, 13] = 0.5 *(nfl_df_18.iat[28, 13] + nfl_df_18.iat[13, 13])
    nfl_df_18.iat[30, 13] = 0.5 *(nfl_df_18.iat[30, 13] + nfl_df_18.iat[15, 13])
    
    nfl_df_18.drop([3, 13, 15], inplace=True)
    #print(nfl_df_18) 
        
    cities_selected = cities_selected.astype({'Population (2016 est.)[8]': int})
    
    nfl_df_18.sort_values(by='team', inplace=True)
    cities_selected.sort_values(by='NFL', inplace=True)    
    nfl_df_18 = nfl_df_18.reset_index()
    cities_selected = cities_selected.reset_index()
    nfl_df_18 = nfl_df_18.drop('index', axis=1)
    cities_selected = cities_selected.drop('index', axis=1)
    #print(cities_selected)
    #print(nfl_df_18)
    
    
    
    #raise NotImplementedError()
    population_by_region = cities_selected['Population (2016 est.)[8]'].to_list() # pass in metropolitan area population from cities
    win_loss_by_region = nfl_df_18['W-L%'].to_list() # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]    

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"
    
    corr, pval=stats.pearsonr(population_by_region, win_loss_by_region)
    return corr 

#print(nfl_correlation())

#q5:

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def sports_team_performance():
    # YOUR CODE HERE
    #need a df with area team name sport name and w-l%
    #average values where a sport has multiple teams in one region
    #Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate
    
    #nhl
      #print(cities.head())
    #print(cities.columns)
    cities_selected = cities[[ 'Metropolitan area', 'NHL','Population (2016 est.)[8]']]
    #print(cities_selected)
    #print all nhl team names 
    #print(cities_selected['NHL'].to_string())
    #clean up NHL team names in cities_selected
    def clean_ct_team_name(pattern):
        replacements = {}
        needs_corr = cities_selected['NHL'].str.contains(pattern, regex=True)
        matching_names = cities_selected.loc[needs_corr, 'NHL']
        for team in list(matching_names):
            team_name = team.split("[")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    cities_selected['NHL'] = cities_selected['NHL'].replace(clean_ct_team_name(r".+note.+"))
    cities_selected['NHL'] = cities_selected['NHL'].replace({"—":""})
    #drop row if column is empty
    cities_selected = cities_selected[cities_selected['NHL'] != '']
    #print(cities_selected[['Metropolitan area','NHL']])
   
    #clean up columns with two or more teams
    #print(cities_selected)   
    #Rangers Islanders Devils is Rangers Islanders and Devils
    #Kings Ducks is Kings & Ducks
    #function to duplicate rows of cities_selected
    def dupl_row(row_index_to_duplicate):
        #row_index_to_duplicate = 0
        # Select the specific row
        row_to_add = cities_selected.iloc[[row_index_to_duplicate]]
        # Concatenate the original DataFrame and the duplicated row(s)
        # ignore_index=True resets the index of the final DataFrame
        duplicated_df = pd.concat([cities_selected, row_to_add], ignore_index=True)
        return duplicated_df
        
    cities_selected = dupl_row(0)
    cities_selected = dupl_row(0)
    cities_selected = dupl_row(1)
    #print(cities_selected.index)
    #Rename the value in column 'NHL' at index '0' to 10
    cities_selected.at[0, 'NHL'] = 'Rangers'
    cities_selected.at[1, 'NHL'] = 'Kings'
    cities_selected.at[28, 'NHL'] = 'Islanders'
    cities_selected.at[29, 'NHL'] = 'Devils'
    cities_selected.at[30, 'NHL'] = 'Ducks'
    #print(cities_selected)
    #print(cities_selected['NHL'].to_string())
       
    
    #print(nhl_df.columns)
    #nhl using 2018 data
    nhl_df_18 = nhl_df.loc[nhl_df['year'] == 2018]
    #print(nhl_df_18.head())
    #print(nhl_df_18['team'].to_string())
    
    #clean up team names remove *
    #team names cleaning, using a function
    def clean_team_name(pattern):
        replacements = {}
        needs_corr = nhl_df_18['team'].str.contains(pattern, regex=True)
        matching_names = nhl_df_18.loc[needs_corr, 'team']
        for team in list(matching_names):
            team_name = team.split("*")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    nhl_df_18['team'] = nhl_df_18['team'].replace(clean_team_name(r"[\w\s]+\*$"))
    #print(nhl_df_18['team'].to_string())
    #drop rows with division 
    df_indexed = nhl_df_18.set_index('team')
    idx_nhl_list = nhl_df_18['team'].tolist()
    #print(df_indexed)
    #print(idx_nhl_list)
    for tm in idx_nhl_list:
        team_name = tm.split(" ")
        if 'Division' in team_name:
            #print(team_name)
            df_indexed.drop([tm], inplace=True)
    
    #print(df_indexed)
    nhl_df_18 = df_indexed.reset_index()
    #print(nhl_df_18)
    
    #create new column with w/l ratio
    nhl_df_18 = nhl_df_18.astype({'W': float, 'L': float})
    nhl_df_18['win/loss ratio'] = (nhl_df_18['W'] / (nhl_df_18['L'] + nhl_df_18['W']))
    #print(nhl_df_18)
    
    
    #Rename the following list of teams in cities_selected
    #function to return dictionary of replacements in cities_selected
    def replacements_dict():
        replacements={}
        cities_nhl_list = cities_selected['NHL'].tolist()
        nhl_teams_list= nhl_df_18['team'].tolist()
        for team in cities_nhl_list:
            for nhl_team in nhl_teams_list:
                team_name = nhl_team.split(" ")
                if team in team_name:
                    replacements[team]=nhl_team
        return replacements 
            
    #print(replacements_dict())        
    #replacements = {'Rangers': 'New York Rangers', 'Kings': 'Los Angeles Kings', 'Sharks':'San Jose Sharks', 'Blackhawks': 'Chicago Blackhawks', 'Stars':'Dallas Stars', 
    #                'Capitals':'Washington Capitals', 'Flyers':'Philadelphia Flyers'}
    cities_selected['NHL'] = cities_selected['NHL'].replace(replacements_dict())
    #print(cities_selected)
    
    #For regions with multiple teams in them such as New York and Los Angeles, you should average out the win loss ratios of individual teams 
    #in those regions
    #drop Anaheim Ducks, New Jersey Devils,  New York Islanders
    cities_selected.drop([28, 29, 30], inplace=True) #keep only new york rangers and los angeles kings
    #print(cities_selected)
    #print(nhl_df_18)   
    nhl_df_18.iat[26, 15] = 0.5 *(nhl_df_18.iat[26, 15] + nhl_df_18.iat[24, 15])
    nhl_df_18.iat[15, 15] = 0.333 *(nhl_df_18.iat[15, 15] + nhl_df_18.iat[14, 15] + nhl_df_18.iat[12, 15] )
    nhl_df_18.drop([24, 14, 12], inplace=True)
    #print(nhl_df_18)
      
    #sort according to teams name both cities_selected and nhl_df_18
    #print(cities_selected)
    cities_selected['NHL'] = cities_selected['NHL'].replace({'Blue Jackets': 'Columbus Blue Jackets', 'Maple Leafs' : 'Toronto Maple Leafs', 
                                                             'Red Wings':'Detroit Red Wings', 'Golden Knights':'Vegas Golden Knights'})
    cities_selected = cities_selected.astype({'Population (2016 est.)[8]': int})
    
    nhl_df_18.sort_values(by='team', inplace=True)
    cities_selected.sort_values(by='NHL', inplace=True)    
    nhl_df_18 = nhl_df_18.reset_index()
    cities_selected = cities_selected.reset_index()
    nhl_df_18 = nhl_df_18.drop('index', axis=1)
    cities_selected = cities_selected.drop('index', axis=1)
    nhl_df_18 = nhl_df_18[[ 'team', 'win/loss ratio']]
    #print(cities_selected)
    #print(nhl_df_18)
    
    cities_nhl = cities_selected
    cities_nhl['win/loss ratio_nhl'] = nhl_df_18['win/loss ratio']
    #print(cities_nhl)
    
    #print(cities_selected_nhl)
    
    #nba
    # YOUR CODE HERE
    #print(cities.head())
    #print(cities.columns)
    cities_selected = cities[[ 'Metropolitan area', 'NBA','Population (2016 est.)[8]']]
    #print(cities_selected)
   
    #clean up NBA team names in cities_selected, remove [note]
    def clean_ct_team_name(pattern):
        replacements = {}
        needs_corr = cities_selected['NBA'].str.contains(pattern, regex=True)
        matching_names = cities_selected.loc[needs_corr, 'NBA']
        for team in list(matching_names):
            team_name = team.split("[")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    cities_selected['NBA'] = cities_selected['NBA'].replace(clean_ct_team_name(r".+note.+"))
    cities_selected['NBA'] = cities_selected['NBA'].replace({"—":""})
    #drop row if column is empty
    cities_selected = cities_selected[cities_selected['NBA'] != '']
    #print(cities_selected)
     
    
    #function to duplicate rows of cities_selected
    def dupl_row(row_index_to_duplicate):
        #row_index_to_duplicate = 0
        # Select the specific row
        row_to_add = cities_selected.iloc[[row_index_to_duplicate]]
        # Concatenate the original DataFrame and the duplicated row(s)
        # ignore_index=True resets the index of the final DataFrame
        duplicated_df = pd.concat([cities_selected, row_to_add], ignore_index=True)
        return duplicated_df
        
    cities_selected = dupl_row(0)
    cities_selected = dupl_row(1)
    
    #print(cities_selected)
    #Rename the value in column 'NBA' at index '0' to 10
    cities_selected.at[0, 'NBA'] = 'Knicks'
    cities_selected.at[1, 'NBA'] = 'Lakers'
    cities_selected.at[28, 'NBA'] = 'Nets'
    cities_selected.at[29, 'NBA'] = 'Clippers'
    
    #print(cities_selected)   
    
    #NBA using 2018 data
    nba_df_18 = nba_df.loc[nba_df['year'] == 2018]
    #print(nba_df_18)
    
    #clean up team names remove * and number
    #team names cleaning, using a function
    def clean_team_name(pattern):
        replacements = {}
        needs_corr = nba_df_18['team'].str.contains(pattern, regex=True)
        matching_names = nba_df_18.loc[needs_corr, 'team']
        for team in list(matching_names):
            team_name = team.split("*")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    nba_df_18['team'] = nba_df_18['team'].replace(clean_team_name(r"[\w\s]+[\*].*"))
    #print(nba_df_18)
    
     #clean up team names remove ( and number
    #team names cleaning, using a function
    def clean_team_name(pattern):
        replacements = {}
        needs_corr = nba_df_18['team'].str.contains(pattern, regex=True)
        matching_names = nba_df_18.loc[needs_corr, 'team']
        for team in list(matching_names):
            team_name = team.split("(")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    nba_df_18['team'] = nba_df_18['team'].replace(clean_team_name(r"[\w\s]+[\(].*"))
    #print(nba_df_18)
    
     #Rename the following list of teams in cities_selected
    #function to return dictionary of replacements in cities_selected
    def replacements_dict():
        replacements={}
        cities_nba_list = cities_selected['NBA'].tolist()
        nba_teams_list= nba_df_18['team'].tolist()
        for team in cities_nba_list:
            for nba_team in nba_teams_list:
                team_name = nba_team.split(" ")
                team_name[-1]=team_name[-1].replace('\xa0', '')
                #print(team_name, team)
                if team in team_name:
                    replacements[team]=nba_team
        return replacements 
            
    #print(replacements_dict())        
    cities_selected['NBA'] = cities_selected['NBA'].replace(replacements_dict())
    cities_selected['NBA'] = cities_selected['NBA'].replace({'Trail Blazers':'Portland Trail Blazers'})
    #print(cities_selected)
     
     #For regions with multiple teams in them you should average out the win loss ratios of individual teams 
    #in those regions
    #drop Los Angeles Clippers,Brooklyn Nets
    cities_selected.drop([28, 29], inplace=True) 
    #print(cities_selected)
    #print(nba_df_18.iat[24, 3], nba_df_18.iat[25, 3])
    #print(nba_df_18)
    nba_df_18 = nba_df_18.astype({'W/L%': float})
    nba_df_18.iat[25, 3] = 0.5 *(nba_df_18.iat[24, 3] + nba_df_18.iat[25, 3])
    nba_df_18.iat[10, 3] = 0.5 *(nba_df_18.iat[10, 3] + nba_df_18.iat[11, 3])
    nba_df_18.drop([24, 11], inplace=True)
    #print(nba_df_18)
     
    
    cities_selected = cities_selected.astype({'Population (2016 est.)[8]': int})
    
    nba_df_18.sort_values(by='team', inplace=True)
    cities_selected.sort_values(by='NBA', inplace=True)    
    nba_df_18 = nba_df_18.reset_index()
    cities_selected = cities_selected.reset_index()
    nba_df_18 = nba_df_18.drop('index', axis=1)
    cities_selected = cities_selected.drop('index', axis=1)
    #print(cities_selected)
    #print(nba_df_18)
    cities_nba = cities_selected
    cities_nba['win/loss ratio_nba'] = nba_df_18['W/L%']
    
    #print(cities_nba)
    
    #mlb
    cities_selected = cities[[ 'Metropolitan area', 'MLB','Population (2016 est.)[8]']]
    #print(cities_selected)
   
    #clean up NBA team names in cities_selected, remove [note]
    def clean_ct_team_name(pattern):
        replacements = {}
        needs_corr = cities_selected['MLB'].str.contains(pattern, regex=True)
        matching_names = cities_selected.loc[needs_corr, 'MLB']
        for team in list(matching_names):
            team_name = team.split("[")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    cities_selected['MLB'] = cities_selected['MLB'].replace(clean_ct_team_name(r".+note.+"))
    cities_selected['MLB'] = cities_selected['MLB'].replace({"—":""})
    #drop row if column is empty
    cities_selected = cities_selected[cities_selected['MLB'] != '']
    #print(cities_selected)
    
    #function to duplicate rows of cities_selected
    def dupl_row(row_index_to_duplicate):
        #row_index_to_duplicate = 0
        # Select the specific row
        row_to_add = cities_selected.iloc[[row_index_to_duplicate]]
        # Concatenate the original DataFrame and the duplicated row(s)
        # ignore_index=True resets the index of the final DataFrame
        duplicated_df = pd.concat([cities_selected, row_to_add], ignore_index=True)
        return duplicated_df
        
    cities_selected = dupl_row(0)
    cities_selected = dupl_row(1)
    cities_selected = dupl_row(2)
    cities_selected = dupl_row(3)
    
    #print(cities_selected)
    #Rename the value in column 'NBA' at index '0' to 10
    cities_selected.at[0, 'MLB'] = 'Yankees'
    cities_selected.at[1, 'MLB'] = 'Dodgers'
    cities_selected.at[2, 'MLB'] = 'Giants'
    cities_selected.at[3, 'MLB'] = 'Cubs'
    
    cities_selected.at[26, 'MLB'] = 'Mets'
    cities_selected.at[27, 'MLB'] = 'Angels'
    cities_selected.at[28, 'MLB'] = 'Athletics'
    cities_selected.at[29, 'MLB'] = 'White Sox'
      
    #print(cities_selected)
    
    #MLB using 2018 data
    mlb_df_18 = mlb_df.loc[mlb_df['year'] == 2018]
    #print(mlb_df_18)
    
    #Rename the following list of teams in cities_selected
    #function to return dictionary of replacements in cities_selected
    def replacements_dict():
        replacements={}
        cities_mlb_list = cities_selected['MLB'].tolist()
        mlb_teams_list= mlb_df_18['team'].tolist()
        for team in cities_mlb_list:
            for mlb_team in mlb_teams_list:
                team_name = mlb_team.split(" ")
                #print(team_name, team) 
                if team.split(" ")[0] in team_name:
                    replacements[team]=mlb_team
        return replacements 
            
    #print(replacements_dict())        
    cities_selected['MLB'] = cities_selected['MLB'].replace(replacements_dict())
    #print(cities_selected)    
    #print(mlb_df_18)
    
    #For regions with multiple teams in them you should average out the win loss ratios of individual teams 
    #in those regions
    #drop New York Mets, Los Angeles Angels, Oakland Athletics, Chicago White Sox 
    cities_selected.drop([26, 27, 28, 29], inplace=True) 
    #print(cities_selected)
    #print(mlb_df_18.iat[24, 3], mlb_df_18.iat[25, 3])
    #print(mlb_df_18)
    mlb_df_18 = mlb_df_18.astype({'W-L%': float})
    mlb_df_18.iat[1, 3] = 0.5 *(mlb_df_18.iat[1, 3] + mlb_df_18.iat[18, 3])
    mlb_df_18.iat[25, 3] = 0.5 *(mlb_df_18.iat[25, 3] + mlb_df_18.iat[13, 3])
    mlb_df_18.iat[28, 3] = 0.5 *(mlb_df_18.iat[28, 3] + mlb_df_18.iat[11, 3])
    mlb_df_18.iat[21, 3] = 0.5 *(mlb_df_18.iat[21, 3] + mlb_df_18.iat[8, 3])
    
    mlb_df_18.drop([18, 13, 11, 8], inplace=True)
    #print(mlb_df_18)
    
    cities_selected = cities_selected.astype({'Population (2016 est.)[8]': int})
    
    mlb_df_18.sort_values(by='team', inplace=True)
    cities_selected.sort_values(by='MLB', inplace=True)    
    mlb_df_18 = mlb_df_18.reset_index()
    cities_selected = cities_selected.reset_index()
    mlb_df_18 = mlb_df_18.drop('index', axis=1)
    cities_selected = cities_selected.drop('index', axis=1)
    #print(cities_selected)
    #print(mlb_df_18)
    cities_mlb = cities_selected
    cities_mlb['win/loss ratio_mlb'] = mlb_df_18['W-L%']
    
    #print(cities_mlb)
    
    #NFL
    cities_selected = cities[[ 'Metropolitan area', 'NFL','Population (2016 est.)[8]']]
    #print(cities_selected)
   
    #clean up NBA team names in cities_selected, remove [note]
    def clean_ct_team_name(pattern):
        replacements = {}
        needs_corr = cities_selected['NFL'].str.contains(pattern, regex=True)
        matching_names = cities_selected.loc[needs_corr, 'NFL']
        for team in list(matching_names):
            team_name = team.split("[")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    cities_selected['NFL'] = cities_selected['NFL'].replace(clean_ct_team_name(r".+note.+"))
    cities_selected['NFL'] = cities_selected['NFL'].replace({"—":""})
    cities_selected.drop([13], inplace=True)
    #print(cities_selected.iat[13,1])
    #drop row if column is empty
    cities_selected = cities_selected[cities_selected['NFL'] != '']
    #print(cities_selected)
    
    #function to duplicate rows of cities_selected
    def dupl_row(row_index_to_duplicate):
        #row_index_to_duplicate = 0
        # Select the specific row
        row_to_add = cities_selected.iloc[[row_index_to_duplicate]]
        # Concatenate the original DataFrame and the duplicated row(s)
        # ignore_index=True resets the index of the final DataFrame
        duplicated_df = pd.concat([cities_selected, row_to_add], ignore_index=True)
        return duplicated_df
        
    cities_selected = dupl_row(0)
    cities_selected = dupl_row(1)
    cities_selected = dupl_row(2)
    
    #Rename the value in column 'NBA' at index '0' to 10
    cities_selected.at[0, 'NFL'] = 'Giants'
    cities_selected.at[1, 'NFL'] = 'Rams'
    cities_selected.at[2, 'NFL'] = '49ers'
    
    cities_selected.at[29, 'NFL'] = 'Jets'
    cities_selected.at[30, 'NFL'] = 'Chargers'
    cities_selected.at[31, 'NFL'] = 'Raiders'
    
    #print(cities_selected)  
     
    #MLB using 2018 data
    nfl_df_18 = nfl_df.loc[nfl_df['year'] == 2018]
    #print(nfl_df_18)    
        
    #clean up team names remove * and +
    #team names cleaning, using a function
    def clean_team_name(pattern):
        replacements = {}
        needs_corr = nfl_df_18['team'].str.contains(pattern, regex=True)
        matching_names = nfl_df_18.loc[needs_corr, 'team']
        for team in list(matching_names):
            team_name = team.split("*")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    nfl_df_18['team'] = nfl_df_18['team'].replace(clean_team_name(r"[\w\s]+\*$"))
    
    def clean_team_name(pattern):
        replacements = {}
        needs_corr = nfl_df_18['team'].str.contains(pattern, regex=True)
        matching_names = nfl_df_18.loc[needs_corr, 'team']
        for team in list(matching_names):
            team_name = team.split("+")
            replacements[team] = team_name[0]
        #print(replacements)
        return replacements      
    nfl_df_18['team'] = nfl_df_18['team'].replace(clean_team_name(r"[\w\s]+\+$"))
    #print(nfl_df_18)    
    
    #drop rows with AFC or NFC 
    df_indexed = nfl_df_18.set_index('team')
    idx_nfl_list = nfl_df_18['team'].tolist()
    #print(df_indexed)
    #print(idx_nhl_list)
    for tm in idx_nfl_list:
        team_name = tm.split(" ")
        if 'AFC' in team_name or 'NFC' in team_name:
            #print(team_name)
            df_indexed.drop([tm], inplace=True)
    
    #print(df_indexed)
    nfl_df_18 = df_indexed.reset_index()
    #print(nfl_df_18)
    
    #Rename the following list of teams in cities_selected
    #function to return dictionary of replacements in cities_selected
    def replacements_dict():
        replacements={}
        cities_nfl_list = cities_selected['NFL'].tolist()
        nfl_teams_list= nfl_df_18['team'].tolist()
        for team in cities_nfl_list:
            for nfl_team in nfl_teams_list:
                team_name = nfl_team.split(" ")
                #print(team_name, team) 
                if team.split(" ")[0] in team_name:
                    replacements[team]=nfl_team
        return replacements 
            
    #print(replacements_dict())        
    cities_selected['NFL'] = cities_selected['NFL'].replace(replacements_dict())
    #print(cities_selected)    
    #print(nfl_df_18)
    
     #For regions with multiple teams in them you should average out the win loss ratios of individual teams 
    #in those regions
    #drop New York Jets, Los Angeles Chargers, Oakland Raiders 
    cities_selected.drop([29, 30, 31], inplace=True) 
    #print(cities_selected)
    #print(nfl_df_18.iat[24, 13], nfl_df_18.iat[25, 13])
    #print(nfl_df_18)
    nfl_df_18 = nfl_df_18.astype({'W-L%': float})
    nfl_df_18.iat[19, 13] = 0.5 *(nfl_df_18.iat[19, 13] + nfl_df_18.iat[3, 13])
    nfl_df_18.iat[28, 13] = 0.5 *(nfl_df_18.iat[28, 13] + nfl_df_18.iat[13, 13])
    nfl_df_18.iat[30, 13] = 0.5 *(nfl_df_18.iat[30, 13] + nfl_df_18.iat[15, 13])
    
    nfl_df_18.drop([3, 13, 15], inplace=True)
    #print(nfl_df_18) 
        
    cities_selected = cities_selected.astype({'Population (2016 est.)[8]': int})
    
    nfl_df_18.sort_values(by='team', inplace=True)
    cities_selected.sort_values(by='NFL', inplace=True)    
    nfl_df_18 = nfl_df_18.reset_index()
    cities_selected = cities_selected.reset_index()
    nfl_df_18 = nfl_df_18.drop('index', axis=1)
    cities_selected = cities_selected.drop('index', axis=1)
    #print(cities_selected)
    #print(nfl_df_18)
    cities_nfl = cities_selected
    cities_nfl['win/loss ratio_nfl'] = nfl_df_18['W-L%']    
    
    #print(cities_nfl)

 #sort according to Metropolitan area
    cities_nhl.sort_values(by='Metropolitan area', inplace=True)
    cities_nba.sort_values(by='Metropolitan area', inplace=True)
    cities_mlb.sort_values(by='Metropolitan area', inplace=True)
    cities_nfl.sort_values(by='Metropolitan area', inplace=True)
    
    #print(cities_nhl.head())
    #print(cities_nba.head())
    #print(cities_mlb.head())
    #print(cities_nfl.head())
    #combine data frames on same metro area
    cities_nhl_nba = pd.merge(cities_nhl, cities_nba, on='Metropolitan area', how='inner')
    cities_nhl_mlb = pd.merge(cities_nhl, cities_mlb, on='Metropolitan area', how='inner')
    cities_nhl_nfl = pd.merge(cities_nhl, cities_nfl, on='Metropolitan area', how='inner')
    
    cities_nba_mlb = pd.merge(cities_nba, cities_mlb, on='Metropolitan area', how='inner')
    cities_nba_nfl = pd.merge(cities_nba, cities_nfl, on='Metropolitan area', how='inner')
    
    cities_mlb_nfl = pd.merge(cities_mlb, cities_nfl, on='Metropolitan area', how='inner')

    #print(cities_nhl_nba)
    
    
    from scipy.stats import ttest_rel
    
    stat,pval_nhl_nba=ttest_rel(cities_nhl_nba['win/loss ratio_nhl'], cities_nhl_nba['win/loss ratio_nba'])
    stat,pval_nhl_mlb=ttest_rel(cities_nhl_mlb['win/loss ratio_nhl'], cities_nhl_mlb['win/loss ratio_mlb'])
    stat,pval_nhl_nfl=ttest_rel(cities_nhl_nfl['win/loss ratio_nhl'], cities_nhl_nfl['win/loss ratio_nfl'])
    
    stat,pval_nba_mlb=ttest_rel(cities_nba_mlb['win/loss ratio_nba'], cities_nba_mlb['win/loss ratio_mlb'])
    stat,pval_nba_nfl=ttest_rel(cities_nba_nfl['win/loss ratio_nba'], cities_nba_nfl['win/loss ratio_nfl'])
    
    stat,pval_mlb_nfl=ttest_rel(cities_mlb_nfl['win/loss ratio_mlb'], cities_mlb_nfl['win/loss ratio_nfl'])
    
    #return 0
    #raise NotImplementedError()
    
    # Note: p_values is a full dataframe, so df.loc["NFL","NBA"] should be the same as df.loc["NBA","NFL"] and
    # df.loc["NFL","NFL"] should return np.nan
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports)
    
     
    p_values.loc["NFL", "MLB"] = pval_mlb_nfl
    p_values.loc["NFL", "NBA"] = pval_nba_nfl
    p_values.loc["NFL", "NHL"] = pval_nhl_nfl
            
    p_values.loc["NBA", "NHL"] = pval_nhl_nba
    p_values.loc["NBA", "NFL"] = pval_nba_nfl
    p_values.loc["NBA", "MLB"] = pval_nba_mlb
    
    p_values.loc["NHL", "NFL"] = pval_nhl_nfl
    p_values.loc["NHL", "NBA"] = pval_nhl_nba
    p_values.loc["NHL", "MLB"] = pval_nhl_mlb
    
    p_values.loc["MLB", "NHL"] = pval_nhl_mlb
    p_values.loc["MLB", "NFL"] = pval_mlb_nfl
    p_values.loc["MLB", "NBA"] = pval_nba_mlb
    
    for sport_x in sports:
        for sport_y in sports:
            print("pval_" + sport_x.lower() + "_" + sport_y)
    
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values

print(sports_team_performance())








