import pandas as pd


#   words selected if NUMWORDS_SURROUNDING = 2
#        v  v     v  v
# w1 w2 w3 w4 wX w6 w7 w8 w9
#             ^
#       word of interest wX

def f(lyric, word):
    lyrlist = str(lyric).split(" ")
    out = " "
    if word not in lyrlist:
        return ""
    idxs = [i for i, e in enumerate(lyrlist) if e == word]
    for i in idxs:
        # bound it
        slicemax = min(i + NUMWORDS_SURROUNDING, len(lyrlist) - 1)
        slicemin = max(i - NUMWORDS_SURROUNDING, 0)
        out += " ".join(lyrlist[slicemin:slicemax+1]) + " "
    return out


def document_generator(df, wordlist):
    for (word, genre) in wordlist:
        yield df.lyrics.apply(f, args=(word,))


NUMWORDS_SURROUNDING = 3
NUMWORDS_PER_GENRE = 15

d = pd.read_csv("proc_csv/LLgenre.csv")

words = []

for genre in d.genre.unique():
    # list of tuples: (word, genre)
    words += [(x, genre) for x in d[d.genre == genre].sort_values("ll", ascending=False).word.head(NUMWORDS_PER_GENRE).tolist()]

d = pd.read_csv("proc_csv/lyrics_clean.csv")
d.dropna()

words = [words[0]]
for i in document_generator(d, words):
    i.to_csv("surrounding_words_raw.csv")




