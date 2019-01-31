# Snooker Prizes
This project connects two areas that I'm big fun of: **Data Science and Snooker**. B-)

It's goal is to **predict snooker player's money prizes in whole season basing on his achievements**.

The code takes data from online resources (using web scraping) from different seasons (you choose which seasons you are interested in!), saves it in tabular form and perform Data Science algorithms. 

The project is written from scratch in Python.

You can read more about this project on my blog: http://klatonomics.com.

## Web scraping

The Python code sends requests to website to download the whole HTML code. HTML code then is being searched for particular information. This search is based on particular tags and their classes. It's quite vulnerable for any format changes on the website (for instance new tables or renamed CSS classes).

For example money prizes are downloaded from this website: https://cuetracker.net/statistics/prize-money/won/season/2018-2019.

All links are configurable as a part of CueTracker.py in Links class:

```
class Links(Enum):
    CENTURIES = "centuries/most-made/"
    TITLES = "tournaments/won/"
    TOURNAMENTS_AND_MATCHES = "matches-and-frames/won/"
    MONEY = "prize-money/won/"
```

## Variables
 * "Name" - player's first name and last name,
 * "Centuries" - how many times player achieved a break with at least 100 points,
 * "T_Played" - how many tournaments player has taken part in,
 * "M_Played" - how many matches player has played,
 * "M_Won" - how many matches player has won,
 * "Titles" - how many tournaments player has won,
 * "Money" - sum of all money prizes (target variable).
 
All values are applicable for chosen seasons. 

## Data
All of data is being fetched from https://cuetracker.net website, when the program us running. Since the data could be heavy (especially whole HTML code) the largest variables are deleted right after their usage.

## Libraries
 * requests - to call GET method on specifil URL 
 * BeautifulSoup - to parse and organise HTML code 
 * Pandas/NumPy - to prepare data for use in DataFrame format
 * SciKit-Learn - to perform Data Science computations
 
 ## TODO
 
 Next big step is to deploy the code on some web app. It would be done probably with Flask.
 
