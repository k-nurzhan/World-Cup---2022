import pandas as pd
from string import ascii_uppercase as alphabet
import pickle
all_tables = pd.read_html('https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup#Group_G')
dict_table = {}
for letter, i in zip(alphabet, range(12,68,7)):
    df = all_tables[i]
    df.rename(columns={df.columns[1]: 'Team'}, inplace=True)
    df.pop('Qualification')
    dict_table[f'Group {letter}'] = df
dict_table['Group A']
with open('dict_table', 'wb') as output:
    pickle.dump(dict_table, output)