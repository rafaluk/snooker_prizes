from CueTracker import CueTracker, Category
import pandas as pd
import numpy as np

_seasons = ['2016-2017']


def fetch_one_column(category):
    cue_tracker = CueTracker(category)
    global _seasons
    cue_tracker.seasons = _seasons
    _pages = cue_tracker.get_pages()
    money_results = cue_tracker.get_results(_pages)
    return money_results


# fetch Money
money = fetch_one_column(Category.MONEY)

# create name list from Money Prizes
names_list = [k for k in money.keys()]
names_list = sorted(names_list)

# create DataFrame with one column - Name
df = pd.DataFrame(data=names_list, columns=["Name"])
print("Names loaded...")

# fetch Centuries
centuries = fetch_one_column(Category.CENTURIES)
df['Centuries'] = df['Name'].map(centuries)
print("Centuries loaded...")

# fetch Tournaments
tournaments = fetch_one_column(Category.TOURNAMENTS_PLAYED)
df['T_Played'] = df['Name'].map(tournaments)
print("Tournaments loaded...")

# fetch Matches Won
matches_won = fetch_one_column(Category.MATCHES_WON)
df['M_Won'] = df['Name'].map(matches_won)
print("Matches Won loaded...")

# fetch Matches Played
matches_played = fetch_one_column(Category.MATCHES_PLAYED)
df['M_Played'] = df['Name'].map(matches_played)
print("Matches Played loaded...")

# fetch Titles
titles = fetch_one_column(Category.TITLES)
df['Titles'] = df['Name'].map(titles)
# df['Titles'] = df['Titles'].replace(np.nan, 0)
print("Titles loaded...")

# map Money to Names in DataFrame as the last variable - feature
df['Money_Prizes'] = df['Name'].map(money)

print(df.head(20))

import matplotlib.pyplot as plt