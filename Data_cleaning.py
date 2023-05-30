import pandas as pd

df_historical_data = pd.read_csv(r'C:\Users\coys7\World-Cup---2022\Data\WC_data.csv')
df_fixture = pd.read_csv(r'C:\Users\coys7\World-Cup---2022\Data\WC_fixture.csv')

df_fixture['home'] = df_fixture['home'].str.strip()
df_fixture['away'] = df_fixture['away'].str.strip()

delete_index = df_historical_data[df_historical_data['home'].str.contains('Sweden') & df_historical_data['away'].str.contains('Austria')].index
df_historical_data.drop(index = delete_index, inplace=True)

df_historical_data['score'] = df_historical_data['score'].str.replace('[^\d–]', '', regex=True)

df_historical_data['home'] = df_historical_data['home'].str.strip()
df_historical_data['away'] = df_historical_data['away'].str.strip()

df_historical_data[['HomeGoals', 'AwayGoals']] =  df_historical_data['score'].str.split('–', expand=True)
df_historical_data.drop('score', axis=1, inplace=True)

df_historical_data.rename(columns={'home': 'HomeTeam', 'away': 'AwayTeam', 'year': 'Year'}, inplace=True)

df_historical_data = df_historical_data.astype({'HomeGoals': int, 'AwayGoals': int, 'Year': int})

df_historical_data['TotalGoals'] = df_historical_data['HomeGoals'] + df_historical_data['AwayGoals']


df_historical_data.to_csv('Data\Clean_WC_data.csv', index=False)
df_fixture.to_csv('Data\clean_WC_fixture.csv', index=False)