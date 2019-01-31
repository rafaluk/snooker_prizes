from CueTracker import CueTracker, Category
import pandas as pd
import numpy as np

seasons = ['2016-2017']

# fetch data for Money Prizes
cueTrackerMoney = CueTracker(Category.MONEY)
cueTrackerMoney.seasons = seasons
pages = cueTrackerMoney.get_pages()
money_results = cueTrackerMoney.get_results(pages)
del cueTrackerMoney, pages

# filter winners, who won less than 20k
money_results = {k: v for k, v in money_results.items()}

# create name list from Money Prizes
names_list = [k for k in money_results.keys()]
names_list = sorted(names_list)

# create DataFrame with one column - Name
df = pd.DataFrame(data=names_list, columns=["Name"])

print("Names loaded...")

# fetch data for Centuries
cueTrackerCenturies = CueTracker(Category.CENTURIES)
cueTrackerCenturies.seasons = seasons
pages = cueTrackerCenturies.get_pages()
cent_results = cueTrackerCenturies.get_results(pages)
del cueTrackerCenturies, pages

# map Centuries to Name
df['Centuries'] = df['Name'].map(cent_results)

print("Centuries loaded...")

# fetch data for Tournaments
cueTrackerTournaments = CueTracker(Category.TOURNAMENTS_PLAYED)
cueTrackerTournaments.seasons = seasons
pages = cueTrackerTournaments.get_pages()
tournaments_results = cueTrackerTournaments.get_results(pages)
del cueTrackerTournaments, pages

# map Tournaments to Name
df['T_Played'] = df['Name'].map(tournaments_results)

print("Tournaments loaded...")

# fetch data for Matches Won
cueTrackerMatchesWon = CueTracker(Category.MATCHES_WON)
cueTrackerMatchesWon.seasons = seasons
pages = cueTrackerMatchesWon.get_pages()
matches_won_results = cueTrackerMatchesWon.get_results(pages)
del cueTrackerMatchesWon, pages

# map Matches Won to Name
df['M_Won'] = df['Name'].map(matches_won_results)

print("Matches Won loaded...")

# fetch data for Match Played
cueTrackerMatchesPlayed = CueTracker(Category.MATCHES_PLAYED)
cueTrackerMatchesPlayed.seasons = seasons
pages = cueTrackerMatchesPlayed.get_pages()
matches_played_results = cueTrackerMatchesPlayed.get_results(pages)
del cueTrackerMatchesPlayed, pages

# map Metches to Name
df['M_Played'] = df['Name'].map(matches_played_results)

print("Matches Played loaded...")

# fetch data for Titles
cueTrackerTitles = CueTracker(Category.TITLES)
cueTrackerTitles.seasons = seasons
pages = cueTrackerTitles.get_pages()
titles_results = cueTrackerTitles.get_results(pages)
del cueTrackerTitles, pages

# map Metches to Name
df['Titles'] = df['Name'].map(titles_results)
df['Titles'] = df['Titles'].replace(np.nan, 0)

print("Titles loaded...")

# map Money to Names in DataFrame as the last variable - feature
df['Money_Prizes'] = df['Name'].map(money_results)

print(df.head(20))

