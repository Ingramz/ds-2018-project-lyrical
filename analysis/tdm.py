import nltk
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


d = pd.read_csv("proc_csv/lyrics_clean.csv")  # .iloc[:200, :]
d = d.dropna()
d["dec"] = d["year"].apply(str).str.slice(0, 3) + "0s"
d = d[d.dec.isin(["1970s", "1980s", "1990s", "2000s", "2010s"])]
stopwords = [st.replace("'", "") for st in
             nltk.corpus.stopwords.words("english")] +\
             ["10", "17", "1st", "20", "2nd", "chorus", "2x", "3x", "30", "4x",
              "repeat", "repeating", "repeats"]

vec = CountVectorizer(stop_words=stopwords, analyzer="word", max_df=0.95,
                      min_df=10, ngram_range=(1, 3), max_features=40000
                      )

# tdm with above parameters gets made and instantly consumed to get just a
# list of ocurrences across all lyrics (of $max_features most seen words)
tdm = vec.fit_transform(d.lyrics).sum(axis=0).tolist()[0]

# short for most frequent words,
mfw = vec.get_feature_names()
with open("wordlist", "w") as f:
    f.write("\n".join(mfw))

# turns out we don't really need to save this aprt,
# just the list of relevant wrds
# mfw_full = pd.Series(tdm.toarray().transpose(), index=allwords)

vec = CountVectorizer(vocabulary=mfw)

genres = d.genre.unique().tolist()
tdm_genre = pd.DataFrame()
for genre in genres:
    tdm_genre[genre] = pd.Series(
        vec.fit_transform(d[d.genre == genre].lyrics).sum(axis=0).tolist()[0],
        index=mfw
        )
tdm_genre = tdm_genre[tdm_genre.sum(axis=1) > 5]
tdm_genre.to_csv("proc_csv/tdm_pergenre.csv")
del tdm_genre

decades = d.dec.unique().tolist()
tdm_decade = pd.DataFrame()
for decade in decades:
    tdm_decade[decade] = pd.Series(
        vec.fit_transform(d[d.dec == decade].lyrics).sum(axis=0).tolist()[0],
        index=mfw
        )
tdm_decade = tdm_decade[tdm_decade.sum(axis=1) > 5]
tdm_decade.to_csv("proc_csv/tdm_perdecade.csv")
del tdm_decade







