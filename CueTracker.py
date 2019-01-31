import requests
from bs4 import BeautifulSoup
from enum import Enum


class CueTracker:

    def __init__(self, category):
        self._seasons = ['2018-2019']
        self._address_begin = "https://cuetracker.net/statistics/"
        self._address_end = "season/"
        self._category = category

    @property
    def seasons(self):
        return self._seasons

    @property
    def category(self):
        return self._category

    @seasons.setter
    def seasons(self, seasons):
        if type(seasons) is list:
            self._seasons = seasons
        else:
            raise TypeError("Seasons must be passed as a list, e.g. ['2017-2018', '2018-2019']")

    @category.setter
    def category(self, value):
        if type(value) is Category:
            self._category = value
        else:
            raise TypeError("Category type must be CueTracker.Category")

    def get_pages(self):
        """Downloads HTML pages within defined seasons."""
        pages = []
        counter = 0
        seasons = self.seasons
        infix = self.category_to_link(self.category).value
        for season in seasons:
            address = self._address_begin + infix \
                      + self._address_end + season
            page = requests.get(address)
            soup = BeautifulSoup(page.content, 'html.parser')
            pages.append(soup)
            counter += 1
            print("<get_pages> " + str(counter) + " of " +
                  str(len(seasons)) + " pages downloaded.")
        return pages

    @staticmethod
    def extract_data(tag_list, threshold, value_cell):
        """Obtains results from <tr> object and adds it to a dictionary.

        Returns a dictionary: results={name:score}."""
        results = {}
        for cell in tag_list:
            inside_cell = list(cell.children)
            value = int(inside_cell[value_cell].get_text().replace(",", ""))
            if value < threshold:
                break
            name = inside_cell[3].find("a").get_text()
            if name in results:
                results[name] += value
            else:
                results[name] = value
        return results

    # @staticmethod
    # def extract_tournaments_played(tag_list, threshold):
    #     """Obtains results from <tr> object and adds it to a dictionary.
    #
    #     Returns a dictionary: results={name:score}."""
    #     results = {}
    #     for cell in tag_list:
    #         inside_cell = list(cell.children)
    #         # print(inside_cell)
    #         value = int(inside_cell[5].get_text())
    #         if value < threshold:
    #             break
    #         name = inside_cell[3].find("a").get_text()
    #         if name in results:
    #             results[name] += value
    #         else:
    #             results[name] = value
    #     return results

    @staticmethod
    def category_to_link(category):
        """Maps enum Category to enum Link.

        Params:
        - category: category to map

        Returns:
        - link from the category"""

        if category == Category.CENTURIES:
            return Links.CENTURIES
        if category == Category.TITLES:
            return Links.TITLES
        if category == Category.MATCHES_WON \
                or category == Category.TOURNAMENTS_PLAYED\
                or category == Category.MATCHES_PLAYED:
            return Links.TOURNAMENTS_AND_MATCHES
        if category == Category.MONEY:
            return Links.MONEY

    @staticmethod
    def merge_dicts(dict1, dict2):
        """Merges two dictionaries.

        If a key is present in both dictionaries,
        then the values from both are added."""

        return {key: dict1.get(key, 0) + dict2.get(key, 0)
                for key in set(dict1) | set(dict2)}

    def get_results(self, pages):
        """Combines results from different seasons (different pages).

        Parameters:
        - pages: HTML objects ready to be extracted from

        Return a list of tuples."""
        if self._category == Category.CENTURIES:
            results_dict = self.combine_results(pages, 5)
        elif self._category == Category.TOURNAMENTS_PLAYED:
            results_dict = self.combine_results(pages, 5)
        elif self._category == Category.MATCHES_PLAYED:
            results_dict = self.combine_results(pages, 7)
        elif self._category == Category.MATCHES_WON:
            results_dict = self.combine_results(pages, 9)
        elif self._category == Category.MONEY:
            results_dict = self.combine_results(pages, 5)

        return results_dict

    def combine_results(self, pages, value_cell):
        results_dict = {}
        for page in pages:
            tr_tags = list(page.find_all('tr'))
            tournaments = self.extract_data(tr_tags, 5, value_cell)
            results_dict = self.merge_dicts(results_dict, tournaments)
        return results_dict


class Category(Enum):
    CENTURIES = 1
    TITLES = 2
    TOURNAMENTS_PLAYED = 3
    MATCHES_PLAYED = 4
    MATCHES_WON = 5
    MONEY = 6


class Links(Enum):
    CENTURIES = "centuries/most-made/"
    TITLES = "tournaments/won/"
    TOURNAMENTS_AND_MATCHES = "matches-and-frames/won/"
    MONEY = "prize-money/won/"
