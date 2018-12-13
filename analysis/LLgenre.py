import pandas as pd
from numpy import log


dg = pd.read_csv("proc_csv/tdm_pergenre.csv")
dout = pd.DataFrame()

# all ocurrences of all words in all genres
total_all = dg.sum().sum()
for genre in dg.columns[1:]:
    # all ocurrences of all words in this genre
    total_in_genre = dg[genre].sum()
    # al ocurrences of all words in other genres
    total_in_other_genres = total_all - total_in_genre

    do2 = pd.DataFrame()
    # add list of words
    do2["word"] = dg["word"]
    # add genre
    do2["genre"] = genre
    # add number of word ocurrences in that genre
    do2["w_occ"] = dg[genre]
    # add number of word occurences in other genres
    do2["w_other_occ"] = dg.drop(columns=[genre]).sum(axis=1)

    do2["expected"] = total_in_genre * (dg.sum(axis=1)/total_all)
    do2["expected_other"] = total_in_other_genres * (dg.sum(axis=1)/total_all)
    do2.loc[do2.w_occ == 0, 'w_occ'] += 0.001
    do2.loc[do2.w_other_occ == 0, 'w_other_occ'] += 0.001
    do2["ll"] = 2 * (do2.w_occ * log(do2.w_occ/do2.expected) +
                     do2.w_other_occ * log(do2.w_other_occ /
                     do2.expected_other))
    do2.loc[do2.w_occ < do2.expected, "ll"] *= -1
    dout = pd.concat([dout, do2])

dout.to_csv("proc_csv/LLgenre.csv", index=False)





