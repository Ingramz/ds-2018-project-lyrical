import pandas as pd
from numpy import log


def get_LL_frame(df: pd.DataFrame, field: str):
    """take in term-document matrix and return log-likelihood dataframe"""

    dout = pd.DataFrame()
    # all ocurrences of all words in all columns
    total_all = dg.sum().sum()
    for col in dg.columns[1:]:
        # all ocurrences of all words in this col
        total_in_col = dg[col].sum()
        # al ocurrences of all words in other cols
        total_in_other_cols = total_all - total_in_col

        do2 = pd.DataFrame()
        # add list of words
        do2["word"] = dg["word"]
        # add col
        do2[field] = col
        # add number of word ocurrences in that col
        do2["w_occ"] = dg[col]
        # add number of word occurences in other cols
        do2["w_other_occ"] = dg.drop(columns=[col]).sum(axis=1)

        do2["expected"] = total_in_col * (dg.sum(axis=1)/total_all)
        do2["expected_other"] = total_in_other_cols *\
            (dg.sum(axis=1)/total_all)

        do2.loc[do2.w_occ == 0, 'w_occ'] += 0.001
        do2.loc[do2.w_other_occ == 0, 'w_other_occ'] += 0.001
        do2["ll"] = 2 * (do2.w_occ * log(do2.w_occ/do2.expected) +
                         do2.w_other_occ * log(do2.w_other_occ /
                         do2.expected_other))
        do2.loc[do2.w_occ < do2.expected, "ll"] *= -1
        dout = pd.concat([dout, do2])
    return dout


# this dataset is actually really bad for year accuracy for some reason
# so I'm leaving this out
# dg = pd.read_csv("proc_csv/tdm_perdecade.csv")
# get_LL_frame(dg, "decade").to_csv("proc_csv/LLdecade.csv", index=False)

dg = pd.read_csv("proc_csv/tdm_pergenre.csv")
dout = get_LL_frame(dg, "genre")
dout.to_csv("proc_csv/LLgenre.csv", index=False)

dfinal = pd.DataFrame()
for i in dg.columns[1:]:
    dfinal = pd.concat([dfinal, dout[dout.genre == i].sort_values("ll",
                        ascending=False).head(50)])
dfinal.to_html("ranked.html")





