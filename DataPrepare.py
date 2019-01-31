from CueTracker import CueTracker, Category
import pandas as pd


class DataPrepare:

    def __init__(self, seasons):
        self._seasons = seasons

    def fetch_one_column(self, category):
        cue_tracker = CueTracker(category)
        cue_tracker.seasons = self._seasons
        _pages = cue_tracker.get_pages()
        money_results = cue_tracker.get_results(_pages)
        print(str(category) + " loaded.")
        return money_results

    def fetch_all(self):
        money = self.fetch_one_column(Category.MONEY)
        centuries = self.fetch_one_column(Category.CENTURIES)
        tournaments = self.fetch_one_column(Category.TOURNAMENTS_PLAYED)
        matches_won = self.fetch_one_column(Category.MATCHES_WON)
        matches_played = self.fetch_one_column(Category.MATCHES_PLAYED)
        titles = self.fetch_one_column(Category.TITLES)

        # create name list from Money Prizes
        names_list = [k for k in money.keys()]
        names_list = sorted(names_list)

        # create DataFrame with one column - Name
        df = pd.DataFrame(data=names_list, columns=["Name"])
        df['Centuries'] = df['Name'].map(centuries)
        df['T_Played'] = df['Name'].map(tournaments)
        df['M_Won'] = df['Name'].map(matches_won)
        df['M_Played'] = df['Name'].map(matches_played)
        df['Titles'] = df['Name'].map(titles)
        df['Money_Prizes'] = df['Name'].map(money)

        return df

    def get_csv_file(self, sep=";"):
        self.fetch_all().to_csv("snooker_data.csv", sep=sep, index=False)
