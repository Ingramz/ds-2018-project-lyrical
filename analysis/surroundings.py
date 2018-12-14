import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import nltk


stopwords = [st.replace("'", "") for st in
             nltk.corpus.stopwords.words("english")] +\
             ["1st", "2nd", "chorus", "2x", "3x", "4x", "x2", "x3",
              "x4", "x5", "x6" "x7", "x8", "repeat", "repeating", "repeats",
              "instrumental", "instruments",
              # the next are rasta stop words... yea we need em
              "da", "mek", "buju", "ina", "seh", "sade", "inna", "jah", "pon",
              "nuh", "yuh", "fi", "di", "mi",
              # misc
              "dm", "gyal", "performed", "im"]

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
        yield df.lyrics.apply(f, args=(word,)).str.cat(sep=" ")


NUMWORDS_SURROUNDING = 2
NUMWORDS_PER_GENRE = 15
NUMWORDS_RELATED = 10

d = pd.read_csv("proc_csv/LLgenre.csv")

words = []

for genre in d.genre.unique():
    # list of tuples: (word, genre)
    words += [(x, genre) for x in d[d.genre == genre].sort_values("ll", ascending=False).word.head(NUMWORDS_PER_GENRE).tolist()]
stopwords += [x[0] for x in words]


d = pd.read_csv("proc_csv/lyrics_clean.csv")
d.dropna()

vec = CountVectorizer(stop_words=stopwords, analyzer="word", max_features=10000)

tdm = vec.fit_transform(document_generator(d, words))
d = pd.DataFrame(tdm.transpose().toarray(), index=vec.get_feature_names(), columns=words)
del tdm

newindex = []
ocurrences = []
genres = []
anchorword = []
for (word, genre) in words:
    toprelatedwords = d[(word, genre)].sort_values(ascending=False).head(NUMWORDS_RELATED)
    newindex += toprelatedwords.index.tolist()
    ocurrences += toprelatedwords.tolist()
    genres += [genre] * NUMWORDS_RELATED
    anchorword += [word] * NUMWORDS_RELATED

out = pd.DataFrame(index=newindex)
out["occ"] = ocurrences
out["genre"] = genres
out["anchor_word"] = anchorword





