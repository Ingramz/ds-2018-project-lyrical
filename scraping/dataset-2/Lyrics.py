# -*- coding: utf-8 -*-
import os
import time
import urllib2
import requests
import pandas as pd
from bs4 import BeautifulSoup
from multiprocessing import Pool
import sys
import gc

base = "http://www.lyrics.com"
files = os.listdir("Data/Songs")
s = requests.Session()

files.sort()

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def scrapeLyrics(x):
	url = x["Url"]

	if(url[:6] == "/lyric"):
		# Continuous tries to avoid breaking in between and without data
		while(True):
			try:
				webp = s.get(base + x['Url'])
				break
			except requests.exceptions.RequestException as e:  # This is the correct syntax
				print(e)
				time.sleep(20)

		# Basic pre processing
		html = webp.content
		soup = BeautifulSoup(html,'lxml', from_encoding="utf-8")
		metas = soup.find('pre', class_="lyric-body")
		year = soup.find('a', {'title': 'See all songs from this year'})
		if year is None:
			year = ''
		else:
			year = year.text

		try:
			print("Indexing " + x["Band"] + " - " + x["Song"])
			return [{
				"Band": x["Band"],
				"Song": x["Song"],
				"Lyrics": metas.text,
				"Year": year
			}]
		except Exception as e:
			print("Didn't work for " + x["Band"] + " - " + x["Song"] + " | " + str(e))
	return []

if __name__ == '__main__':
        i = 0
	p = Pool(100)
	for file in files:
		print("Working for " + file)
		data = pd.read_csv("Data/Songs/" + file)
		for x in batch(data.to_dict('records'), 1000):
			l = p.map(scrapeLyrics, x)
			flat_list = [item for sublist in l for item in sublist]
			df1 = pd.DataFrame(flat_list)
		        i = i + 1
			df1.to_csv("Data/Lyrics/LyricsBatch" + str(i) + ".csv", index = False, encoding = 'utf-8')
			del df1
			gc.collect()
