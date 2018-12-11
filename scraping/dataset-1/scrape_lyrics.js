const rp = require('request-promise-native');
const cheerio = require('cheerio');
const Papa = require('papaparse')
const fs = require('fs')
var Iconv  = require('iconv').Iconv;
var iconv = new Iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE');
const Json2csvParser = require('json2csv').Parser;

function normalize_song(song) {
  let title = iconv.convert(
    song.title
      .replace(/"/g, '')
      .toLowerCase()
      .replace(/[^a-z0-9 ]+/g, ' ')
  ).toString().replace(/'/g, '').trim()

  let artist = iconv.convert(
    song.artist
      .replace(/"/g, '')
      .toLowerCase()
      .replace(/[^a-z0-9 ]+/g, ' ')
  ).toString().replace(/'/g, '').split(/ featuring | feat | feat\. | with | duet | and /)[0].trim()

  return {title, artist}
}

function strip_the(song)
{
  let title = song.title.replace(/the /g, '')
  let artist = song.artist.replace(/the /g, '')
  return {title, artist}
}

async function scrape_metrolyrics(song) {
  let artist = song.artist.replace(/ +/g, '-')
  let title = song.title.replace(/ +/g, '-')

  const options = {
    uri: `http://metrolyrics.com/${title}-lyrics-${artist}.html`,
    transform: function (body) {
      return cheerio.load(body);
    }
  }

  try {
    let $ = await rp(options)
    let lyrics = $('#lyrics-body-text .verse').map((i, e) => $(e).text()).get().join(' ').replace(/\s+/g, ' ').trim()
    if (lyrics) {
      return {lyrics, source: options.uri}
    }
  } catch {

  }
  return false
}

async function scrape_songlyrics(song) {
  let artist = song.artist.replace(/ +/g, '-')
  let title = song.title.replace(/ +/g, '-')

  const options = {
    uri: `http://songlyrics.com/${artist}/${title}-lyrics`,
    transform: function (body) {
      return cheerio.load(body);
    }
  }

  try {
    let $ = await rp(options)
    let lyrics = $('#songLyricsDiv').map((i, e) => $(e).text()).get().join(' ').replace(/\s+/g, ' ').trim()
    if (lyrics) {
      return {lyrics, source: options.uri}
    }
  } catch {

  }
  return false
}

async function scrape_lyricsmode(song) {
  let artist = song.artist.replace(/ +/g, '_')
  let title = song.title.replace(/ +/g, '_')
  let firstletter = artist[0]

  const options = {
    uri: `http://www.lyricsmode.com/lyrics/${firstletter}/${artist}/${title}.html`,
    transform: function (body) {
      return cheerio.load(body);
    }
  }

  try {
    let $ = await rp(options)
    let lyrics = $('#lyrics_text').map((i, e) => $(e).text()).get().join(' ').replace(/\s+/g, ' ').trim()
    if (lyrics) {
      return {lyrics, source: options.uri}
    }
  } catch {

  }
  return false
}

async function scrape_genius(song) {
  let artist = song.artist.replace(/ +/g, '-')
  let title = song.title.replace(/ +/g, '-')

  const options = {
    uri: `https://genius.com/${artist}-${title}-lyrics`,
    transform: function (body) {
      return cheerio.load(body);
    }
  }

  try {
    let $ = await rp(options)
    let lyrics = $('.lyrics p').map((i, e) => $(e).text()).get().join(' ').replace(/\s+/g, ' ').trim()
    if (lyrics) {
      return {lyrics, source: options.uri}
    }
  } catch {

  }
  return false
}

async function scrape_from_url(song) {
  if (!song.source) {
    return false
  }

  const providers = [
    {domain: 'genius.com', selector: '.lyrics p'},
    {domain: 'lyricsmode.com', selector: '#lyrics_text'},
    {domain: 'songlyrics.com', selector: '#songLyricsDiv'},
    {domain: 'metrolyrics.com', selector: '#lyrics-body-text .verse'}
  ]

  for (provider of providers) {
    if (song.source.indexOf(provider.domain) === -1) {
      continue
    }

    let options = {
      uri: song.source,
      transform: function (body) {
        return cheerio.load(body);
      }
    }

    try {
      let $ = await rp(options)
      let lyrics = $(provider.selector).map((i, e) => $(e).text()).get().join(' ').replace(/\s+/g, ' ').trim()
      if (lyrics) {
        return {lyrics, source: options.uri}
      }
    } catch (e) {
    }
  }

  return false
}

const chunk = function(array, size) {
  if (!array.length) {
    return [];
  }
  const head = array.slice(0, size);
  const tail = array.slice(size);

  return [head, ...chunk(tail, size)];
};

async function scrape_single(song) {
  let lyrics = await scrape_from_url(song)
            || await scrape_metrolyrics(normalize_song(song))
            || await scrape_songlyrics(normalize_song(song))
            || await scrape_lyricsmode(normalize_song(song))
            || await scrape_genius(normalize_song(song))
            || await scrape_metrolyrics(strip_the(normalize_song(song)))
            || await scrape_songlyrics(strip_the(normalize_song(song)))
            || await scrape_lyricsmode(strip_the(normalize_song(song)))
            || await scrape_genius(strip_the(normalize_song(song)))

  if (lyrics) {
    song.lyrics = lyrics.lyrics
    song.source = lyrics.source
  }

  return song
}

async function scrape() {
  let songs = chunk(Papa.parse(fs.readFileSync('top_songs.csv','UTF-8').trim(), {delimiter: ',', header: true}).data, 100)
  let results = []
  let total = 0
  for (song of songs) {
    let promises = []
    for (single of song) {
      if(single.lyrics.length > 0) {
        results.push([single])
      } else {
        promises.push(scrape_single(single))
      }
    }
    results.push(await Promise.all(promises))
    total += promises.length
    console.log(total)
  }

  const fields = ['year', 'ranking', 'artist', 'title', 'lyrics', 'source']
  const json2csvParser = new Json2csvParser({ fields })
  const csv = json2csvParser.parse(results.reduce((acc, val) => acc.concat(val), []))

  fs.writeFileSync('songs-lyrics.csv', csv)
}

scrape()
