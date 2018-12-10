from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd
import urllib


def get_urlstring(base_url, row):
    return base_url + urllib.parse.quote_plus(row.artist + " " + row.song)


searchbaseurl = "https://www.allmusic.com/search/songs/"
ua = UserAgent()

d = pd.read_csv("raw_csv/songdata.csv").iloc[10:15, :]
for i, row in d.iterrows():

    # get the search results page
    url = get_urlstring(searchbaseurl, row)
    r = requests.get(url, headers={"User-Agent": ua.random})
    if r.status_code != 200:
        print("Rejected: status code {}".format(r.status_code))
        continue

    # parse
    soup = BeautifulSoup(r.text, 'html.parser')

    # get candidates( many artists )
    songcandidates = soup.find_all("li", {"class": "song"})
    artists = []
    titles = []
    for elem in songcandidates:
        performers = elem.find("div", {"class": "performers"})
        if not performers:
            artists.append([])
            titles.append([])
            continue
        titles.append(elem.find("div", {"class": "title"}).a.string)
        artists.append([x.string for x in performers.find_all("a")])
    print(titles)
    print(artists)

    years = [x.string for x in soup.find_all("td", {"class": "year"})]





