# LYRICAL

[Project registration slide](https://docs.google.com/presentation/d/1RHDUPsJVVtwVfPp8-WxsK8udEpYOmf4Ki9NjtbgpLDU/edit#slide=id.g48274606ac_165_0)



## Data gathering report:
Since this is more of an exploratory project rather than business-oriented of predictive, the requirements are not too severe: all that's needed are some basic information such as artist name, year of release, and song title to go along with the all-important lyrics themselves. The data are luckily readily available in web-crawlable format on the internet. Other possibly useful information would have been keys, chords, and album names, but such information are not easily available and would add a comparatively small amount compared to lyrics, so they are not being considered.
3 of the 4 datasets require considerable cleaning if they're to be used: the lyrics field contains separators, newlines, and other characters prone to misbehaviour, however, this is routine data preparation and does not present an insurmountable problem.

### [Dataset 1](https://github.com/walkerkq/musiclyrics)
A compilation of every song in billboard's year-end top 100 list since 1965 until 2015, as well as their lyrics. Also contains some additional word frequency analysis. Note: in pandas, we must add encoding="latin1" when reading the csv.
#### Main file: billboard_lyrics_1964-2015.csv.
Features:
- Rank: Rank that year, out of 100.
-Song title.
- Artist: Artist responsible for the song. Collaboration and featuring credits cause a little bit of noise, which we may be able to clean up slightly.
- Year released.
- Full lyrics: All non-capitalized, no punctuation (including apostrophes) or newlines other than normal spaces between words.
- Source: A categorical describing website source for the lyrics. 1 is metrolyrics.com, 3 is songlyrics.com and 5 is lyricsmode.com. Websites were chosen for ease of webcrawling.

#### Secondary files:
   tdm_bydecade.csv. A term-document matrix with all non-sparse n-grams (n up to 4), counted by decade. That is, sequential combinations of up to 4 words. Each row represents a single n-gram, and the columns contain the number of time they occur in lyrics from the 60s, 70s, 80s, 90s, 00s, and 2010s.

LL_bydecade.csv. Calculated from the term-document matrix, the log-likelihood of each word for each decade.
Features:
- Year: Decade being considered for the following columns.
- Keyword: n-gram in question (n in [1,4])
- LL: log likelihood for word in this decade, relative to other decades. Calculated as 2 * (o1 * log(o1/e1) + o2 * log(o2/e2))
- o1: total appearances of that word in the given decade.
- o2: total appearances of that word in all other decades.
- e1: expected appearances of that word in the given decade, calculated as (total probability of word considering all decades * total amount of words in the given decade)
- e2: expected appearances of that word in all other decades, calculated as (total probability of word considering all decades * total amount of words in all other decades)

LL_bydecade_ranked.csv. Same features as above, but only contains the 25 top ranked likelihood n-grams for each decade, and an additional feature containing that rank.



### [Dataset 2](https://www.kaggle.com/artimous/every-song-you-have-heard-almost)
A simpler dataset taken from lyrics.com, but with many more assorted songs since these aren't limited to top 100 hits, or hits at all. These will require substantial cleaning, since they are improperly separated as csvs.
Features:
- Artist
- Lyrics
- Song title

### [Dataset 3](https://www.kaggle.com/gyani95/380000-lyrics-from-metrolyrics)
Another simple yet ample dataset with ample need of cleaning, since the lyrics contain csv separators.
Features:
- Index.
- Song title: With hyphen-separated words and no capitalization.
- Year of release
- Artist: Also hyphen-separated.
- Genre.
- Lyrics.

### [Dataset 4](https://www.kaggle.com/mousehead/songlyrics)
Same as above, from lyricsfreak.com. We might not need to use all the datasets — there's bound to be duplicates.
Features:
- Artist.
- Song title.
- Link ending.
- Lyrics.
