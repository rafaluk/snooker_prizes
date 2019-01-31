# main_address = "https://cuetracker.net" \
#                "/statistics/centuries/most-made/season/"
# 2018-2019 - po sleszu
#
# all_seasons = ["2014-2015",
#                "2015-2016",
#                "2016-2017",
#                "2017-2018",
#                "2018-2019"]
#
#
# def get_pages(seasons, prefix):
#     """Downloads HTML pages within defined seasons."""
#     pages = []
#     counter = 0
#     for season in seasons:
#         address = prefix + season
#         page = requests.get(address)
#         soup = BeautifulSoup(page.content, 'html.parser')
#         pages.append(soup)
#         counter += 1
#         print("<get_pages> " + str(counter) + " of " +
#               str(len(seasons)) + " pages downloaded.")
#     return pages
#
#
# def get_centuries(tag_list):
#     """Obtains results from <tr> object and adds it to a dictionary.
#
#     Returns a dictionary: results={name:score}."""
#     results = {}
#     centuries_threshold = 20
#     for cell in tag_list:
#         inside_cell = list(cell.children)
#         score = int(inside_cell[5].get_text())
#         if score < centuries_threshold:
#             break
#         name = inside_cell[3].find("a").get_text()
#         if name in results:
#             results[name] += score
#         else:
#             results[name] = score
#     return results
#
#
# def merge_dicts(dict1, dict2):
#     """Merges two dictinaries.
#
#     If a key is present in both dictionaries,
#     then the values from both are added."""
#     return {key: dict1.get(key, 0) + dict2.get(key, 0)
#             for key in set(dict1) | set(dict2)}



# from operator import itemgetter
# a = {"a": 1, "b": 2}
# b = {"a": 2, "b": 10, "c": 2}
# sz = merge_dicts(a,b)
# print(sz)
# bb= sorted(sz.items(), key=itemgetter(1))
# print(bb)


# def combine_results(pages):
#     """Combines results from different seasons (different pages).
#
#     Return a list of tuples."""
#     score_dict = {}
#     for page in pages:
#         tr_tags = list(page.find_all('tr'))
#         scores = get_centuries(tr_tags)
#         score_dict = merge_dicts(score_dict, scores)
#     return score_dict

from CueTracker import CueTracker, Category
import pandas as pd

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

# map Money to Names in DataFrame
df['Money_Prizes'] = df['Name'].map(money_results)

print(df.head(10))

# fetch data for Centuries
cueTrackerCenturies = CueTracker(Category.CENTURIES)
cueTrackerCenturies.seasons = seasons
pages = cueTrackerCenturies.get_pages()
cent_results = cueTrackerCenturies.get_results(pages)
del cueTrackerCenturies, pages

# map Centuries to Name
df['Centuries'] = df['Name'].map(cent_results)

print(df.head(10))

# fetch data for Tournaments
cueTrackerTournaments = CueTracker(Category.TOURNAMENTS_PLAYED)
cueTrackerTournaments.seasons = seasons
pages = cueTrackerTournaments.get_pages()
tournaments_results = cueTrackerTournaments.get_results(pages)
del cueTrackerTournaments, pages

# map Tournaments to Name
df['T_Played'] = df['Name'].map(tournaments_results)

print(df.head(10))

# fetch data for Matches Won
cueTrackerMatchesWon = CueTracker(Category.MATCHES_WON)
cueTrackerMatchesWon.seasons = seasons
pages = cueTrackerMatchesWon.get_pages()
matches_won_results = cueTrackerMatchesWon.get_results(pages)
del cueTrackerMatchesWon, pages

# map Matches Won to Name
df['M_Won'] = df['Name'].map(matches_won_results)

print(df.head(10))

# fetch data for Match Played
cueTrackerMatchesPlayed = CueTracker(Category.MATCHES_PLAYED)
cueTrackerMatchesPlayed.seasons = seasons
pages = cueTrackerMatchesPlayed.get_pages()
matches_played_results = cueTrackerMatchesPlayed.get_results(pages)
del cueTrackerMatchesPlayed, pages

# map Metches to Name
df['M_Played'] = df['Name'].map(matches_played_results)

print(df.head(10))

# df.to_csv("chuj.csv", index=False)