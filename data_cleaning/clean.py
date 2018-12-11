import pandas as pd
from multiprocessing import Pool, cpu_count
import numpy as np
import langid

csv_input_path = "raw_csv/"
csv_output_path = "proc_csv/"


# ugly copypaste
def rep_songdata(df):

    df = df.dropna()
    # clear out non-english songs
    i_to_drop = []
    for i, r in df.iterrows():
        lyr = str(r["text"])
        if not lyr or langid.classify(lyr)[0] != 'en':
            i_to_drop.append(i)
    df = df.drop(i_to_drop)

    # remove accents and unicode weirdness
    for col in df.columns:
        df[col] = df[col].str.normalize('NFKD')\
                         .str.encode('ascii', errors='ignore',)\
                         .str.decode('utf-8')
        df[col] = df[col].str.lower().str.strip()

    # remove most punctuation
    df.loc[:, df.columns != "link"] = df.loc[:, df.columns != "link"]\
        .replace("[=+)(*&^%$#@!~?;\":><,./]", " ", regex=True)

    df.loc[:, df.columns != "link"] = df.loc[:, df.columns != "link"]\
        .replace("['`]", "", regex=True)

    # replace dashes, carriage returns, newlines with spaces
    df.loc[:, df.columns != "link"] = df.loc[:, df.columns != "link"]\
        .replace("[-\r\n]", " ", regex=True)

    # remove stuff between brackets (usually something like [chorus]
    df = df.replace("\[.*?\]", " ", regex=True)

    # remove sequences of 2+ spaces
    df = df.replace(" {2,}", " ", regex=True)

    return df


def rep_lyrics(df):

    df = df.dropna()

    # remove non-english songs
    i_to_drop = []
    for i, r in df.iterrows():
        lyr = str(r["lyrics"])
        if not lyr.strip() or langid.classify(lyr)[0] != 'en':
            i_to_drop.append(i)
    df = df.drop(i_to_drop)

    for col in ["song", "artist", "genre", "lyrics"]:
        # remove accents and unicode weirdness
        df[col] = df[col].str.normalize('NFKD')\
                         .str.encode('ascii', errors='ignore',)\
                         .str.decode('utf-8')

        # lowercase it
        df[col] = df[col].str.lower().str.strip()

        # remove most punctuation
        df[col] = df[col].str.replace("[=+)(*&^%$#@!~?;\":><,./]",
                                      " ",
                                      regex=True)

        df[col] = df[col].str.replace("['`]", "", regex=True)

        # replace dashes, carriage returns, newlines with spaces
        df[col] = df[col].str.replace("[-\r\n]", " ", regex=True)

        # remove stuff between brackets (usually something like [chorus]
        df[col] = df[col].str.replace("\[.*?\]", " ", regex=True)

        # remove sequences of 2+ spaces
        df[col] = df[col].replace(" {2,}", " ", regex=True)

    return df


def rep_Lyrics(df):

    df = df.dropna()

    # clear out non-english songs
    i_to_drop = []
    for i, r in df.iterrows():
        lyr = str(r["Lyrics"])
        if not lyr or langid.classify(lyr)[0] != 'en':
            i_to_drop.append(i)
    df = df.drop(i_to_drop)

    # remove most punctuation
    df = df.replace("[=+)(*&^%$#@!~?;\":><,./]", " ", regex=True)

    df = df.replace("[`']", "", regex=True)

    # replace dashes, carriage returns, newlines with spaces
    df = df.replace("[-\r\n]", " ", regex=True)

    # remove stuff between brackets (usually something like [chorus]
    df = df.replace("\[.*?\]", " ", regex=True)

    # remove sequences of 2+ spaces
    df = df.replace(" {2,}", " ", regex=True)

    # remove accents and unicode weirdness
    for col in df.columns:
        df[col] = df[col].str.normalize('NFKD')\
                         .str.encode('ascii', errors='ignore',)\
                         .str.decode('utf-8')
        df[col] = df[col].str.lower().str.strip()

    return df


def fix_strings(df, func):
    # parallelize it
    data_split = np.array_split(df, parts)
    pool = Pool(cores)
    df = pd.concat(pool.map(func, data_split))
    return df


parts = 10
cores = cpu_count()

# ######## For Lyrics1.csv and Lyrics2.csv #########
# data = pd.read_csv(csv_input_path + "Lyrics1.csv", na_values=[" ", "\n", ""])
# data2 = pd.read_csv(csv_input_path + "Lyrics2.csv", na_values=[" ", "\n", ""])
# data = pd.concat([data, data2])
# # for testing purposes:
# # data = data.iloc[:2000, :]
# data = fix_strings(data, rep_Lyrics)
# data.to_csv(csv_output_path + "Lyrics_clean_concat.csv", index=False)

# # ######## For songdata.csv #########
# data = pd.read_csv(csv_input_path + "songdata.csv", na_values=[" ", "\n", ""])
# # test
# # data = data.iloc[:2000, :]
# data = fix_strings(data, rep_songdata)
# data.to_csv(csv_output_path + "songdata_clean.csv", index=False)

# ######## For lyrics.csv #########
data = pd.read_csv(csv_input_path + "lyrics.csv", index_col="index",
                   na_values=[" ", "\n", ""])
# data = data.iloc[:2000, :]
data = fix_strings(data, rep_lyrics)
data.to_csv(csv_output_path + "lyrics_clean.csv", index=False)
