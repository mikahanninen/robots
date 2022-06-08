from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
import re

WEB = Selenium()
HTTP = HTTP()
URL = "https://www.football-data.co.uk/englandm.php"
regex = ".*\/SEASON\/.*\.csv"


def get_csv_files_for_a_season(season: str):
    links = WEB.get_webelements("//a")
    hrefs = [l.get_attribute("href") for l in links]
    matcher = regex.replace("SEASON", season)
    season_links = []
    for href in hrefs:
        if re.match(matcher, href):
            season_links.append(href)
    return season_links


def minimal_task():
    WEB.open_available_browser(URL)
    season = "2122"
    files = get_csv_files_for_a_season(season)
    for f in files:
        filename = f.rsplit("/", 1)[-1]
        HTTP.download(f, filename)
    print("Done.")


if __name__ == "__main__":
    minimal_task()
