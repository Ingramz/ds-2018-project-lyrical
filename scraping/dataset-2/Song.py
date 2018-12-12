# -*- coding: utf-8 -*-

#
#	Script to get song urls and store in
#	batches of 5000 in the Data folder using
#	ArtistUrl.csv. The data is scraped over from
#	lyrics.com
#

import time
import string
import urllib2
import requests
import pandas as pd
from bs4 import BeautifulSoup
from multiprocessing import Pool
import sys
import gc

base = "http://www.lyrics.com/"

# Data frame with all the artist data in Band name -> Url format
df = pd.read_csv("Data/Artists/ArtistUrl.csv")

s = requests.Session()

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def scrapeSong(i):
	print("Working for " + df['Artist'][i] + ", i : " + str(i))

	# Continuous tries to avoid breaking in between and without data
	while(True):
		try:
			webp = s.get(base + df['Urls'][i])
			break
		except requests.exceptions.RequestException as e:  # This is the correct syntax
			print(e)
			time.sleep(20)

	# Basic pre processing
	html 	= webp.content
	soup 	= BeautifulSoup(html,'lxml',from_encoding="utf-8")
	metas 	= soup.findAll('table', class_="tdata")

	results = []
	for meta in metas:
		# Getting all anchor tags representing songs (huge!!!)
		rows 	= meta.findAll('a')

		try:
			for x in rows:
				res = {
					'Band': df['Artist'][i],
					'Url': x['href'],
					'Song': x.find(text=True).encode('utf-8')
				}
				results.append(res.copy())
		except Exception as e:
			print(e)

	# Log comment
	print("Done for " + df['Artist'][i])
	print("Total songs : " + str(len(results)))
	return results

if __name__ == '__main__':
        i = 0
	p = Pool(100)
	for x in batch(range(0, len(df)), 2000):
		l = p.map(scrapeSong, x)
		flat_list = [item for sublist in l for item in sublist]
		df1 = pd.DataFrame(flat_list)
                i = i + 1
		df1.to_csv("Data/Songs/SongData" + str(i) + ".csv", index = False, encoding = 'utf-8')
		del df1
		gc.collect()
