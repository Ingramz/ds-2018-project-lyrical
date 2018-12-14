import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


d = pd.read_csv("proc_csv/lyrics_clean.csv").iloc[:55000, :]
d = d.dropna()
d["dec"] = d["year"].apply(str).str.slice(0, 3) + "0s"
d = d[d.dec.isin(["1970s", "1980s", "1990s", "2000s", "2010s"])]
stopwords = [st.replace("'", "") for st in
             nltk.corpus.stopwords.words("english")] +\
             ["1st", "2nd", "chorus", "2x", "3x", "4x", "x2", "x3",
              "x4", "x5", "x6" "x7", "x8", "repeat", "repeating", "repeats",
              "instrumental", "instruments",
              # the next are rasta stop words... yea we need em
              "da", "mek", "buju", "ina", "seh", "sade", "inna", "jah", "pon",
              "nuh", "yuh", "fi", "di", "mi",
              # misc
              "dm", "gyal", "performed"]

vec = TfidfVectorizer(stop_words=stopwords, analyzer="word", max_df=0.90,
                      min_df=10, ngram_range=(1, 3), max_features=150000)

# tdm with above parameters gets made and instantly consumed to get just a
# list of ocurrences across all lyrics (of $max_features most seen n-grams)
tdm = vec.fit_transform(d.lyrics)

model = KMeans(n_clusters=6, init='k-means++', max_iter=100, n_init=1)
model.fit(tdm)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vec.get_feature_names()
for i in range(6):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print

