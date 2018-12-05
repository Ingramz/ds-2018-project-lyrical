import pandas as pd
import numpy as np

# Band, Lyrics, Song
data1 = pd.read_csv("proc_csv/Lyrics_clean_concat.csv")

# artist, song, link, text
data2 = pd.read_csv("proc_csv/songdata_clean.csv")

# index, song, year, artist, genre, lyrics
data3 = pd.read_csv("proc_csv/lyrics_clean.csv")

data1.columns = ["artist", "lyrics", "song"]
data1["link"] = ""
data1["genre"] = ""
data1["year"] = ""

data2.columns = ["artist", "song", "link", "lyrics"]
data2["genre"] = ""
data2["year"] = np.nan

data3["link"] = ""
data3.drop(["index"], axis=1)

data = pd.concat([data1, data2, data3])
print(data.shape)  # 756766
data.drop_duplicates(["song", "artist"], inplace=True)
print(data.shape)  # 605160
# probably leaves a number of duplicates still in due
# to mistakes in artist and song name
