import pandas as pd
import pickle
from scipy.stats import poisson

dict_table = pickle.load(open(r'C:\Users\coys7\World-Cup---2022\Data\dict_table', 'rb'))
df_historical_data = pd.read_csv(r'C:\Users\coys7\World-Cup---2022\Data\Clean_WC_data.csv')
df_fixture = pd.read_csv(r'C:\Users\coys7\World-Cup---2022\Data\clean_WC_fixture.csv')

df_home = df_historical_data[['HomeTeam', 'HomeGoals', 'AwayGoals']]
df_away = df_historical_data[['AwayTeam', 'HomeGoals', 'AwayGoals']]

df_home  = df_home.rename(columns={'HomeTeam' : 'Team', 'HomeGoals': 'GoalsScored', 'AwayGoals': 'GoalsConceded'})
df_away = df_away.rename(columns={'AwayTeam' : 'Team', 'AwayGoals': 'GoalsScored', 'HomeGoals': 'GoalsConceded'})

df_team_strength = pd.concat([df_home, df_away], ignore_index=True).groupby('Team').mean()


def predict_points(home, away):
    if home in df_team_strength.index and away in df_team_strength.index:
        lamb_home = df_team_strength.at[home, 'GoalsScored']*df_team_strength.at[away, 'GoalsConceded']
        lamb_away = df_team_strength.at[away, 'GoalsScored']*df_team_strength.at[home, 'GoalsConceded']
        prob_home, prob_away, prob_draw = 0, 0, 0
        for x in range(0,11): #number of goals home team
            for y in range(0,11): #number of goals away team
                p = poisson.pmf(x, lamb_home) * poisson.pmf(y, lamb_away)
                if x==y:
                    prob_draw += p
                elif x > y:
                    prob_home += p 
                else:
                    prob_away += p
        
        points_home = 3 * prob_home + prob_draw
        points_away = 3 * prob_away + prob_draw 
        return (points_home, points_away)
    else:
        return(0,0) #Qatar never played in WC
    
#splitting fixture into group, knockout ...
df_fixture_group_48 = df_fixture[:48].copy()
df_fixture_knockout = df_fixture[48:56].copy()
df_fixture_quarter = df_fixture[56:60].copy()
df_fixture_semi = df_fixture[60:62].copy()
df_fixture_finale = df_fixture[62:].copy()


#simulate all matches in group stage
for group in dict_table:
    teams_in_group = dict_table[group]['Team'].values
    df_fixture_group_6 = df_fixture_group_48[df_fixture_group_48['home'].isin(teams_in_group)]
    for index, row in df_fixture_group_6.iterrows():
        home,away = row['home'], row['away']
        points_home, points_away = predict_points(home, away)
        dict_table[group].loc[dict_table[group]['Team'] == home, 'Pts'] += points_home
        dict_table[group].loc[dict_table[group]['Team'] == away, 'Pts'] += points_away
    
    dict_table[group] = dict_table[group].sort_values('Pts', ascending=False).reset_index()
    dict_table[group] = dict_table[group][['Team','Pts']]
    dict_table[group] = dict_table[group].round(0)


#knock-out stages
#update fixtures with group winners
for group in dict_table:
    group_winner = dict_table[group].loc[0,'Team']
    runners_up = dict_table[group].loc[1,'Team']
    df_fixture_knockout.replace({f'Winners {group}': group_winner, f'Runners-up {group}': runners_up}, inplace=True)

df_fixture_knockout['winner'] = '?'

#create winner function
def get_winner(df_fixture_updated):
    for index, row in df_fixture_updated.iterrows():
        home, away = row['home'], row['away']
        points_home, points_away = predict_points(home, away)
        if points_home > points_away:
            winner = home
        else:
            winner = away
        df_fixture_updated.loc[index,'winner'] = winner
    return df_fixture_updated

get_winner(df_fixture_knockout)

#quater-finales
def update_table(df_fixture_round_1, df_fixture_round_2):
    for index, row in df_fixture_round_1.iterrows():
        winner = df_fixture_round_1.loc[index, 'winner']
        match = df_fixture_round_1.loc[index, 'score']
        df_fixture_round_2.replace({f'Winners {match}':winner}, inplace = True)
    df_fixture_round_2['winner'] = '?'
    return df_fixture_round_2

update_table(df_fixture_knockout, df_fixture_quarter)
get_winner(df_fixture_quarter)

#semi_final
update_table(df_fixture_quarter, df_fixture_semi)
get_winner(df_fixture_semi)

#finale
update_table(df_fixture_semi, df_fixture_finale)
print(get_winner(df_fixture_finale.loc[[63]]))