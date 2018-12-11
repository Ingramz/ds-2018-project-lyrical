const rp = require('request-promise-native');
const cheerio = require('cheerio');
const Json2csvParser = require('json2csv').Parser;
const fs = require('fs')

function trim2 (s, c) {
  if (c === "]") c = "\\]";
  if (c === "\\") c = "\\\\";
  return s.replace(new RegExp(
    "^[" + c + "]+|[" + c + "]+$", "g"
  ), "");
}

async function scrape (year) {
  const options = {
    uri: `http://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_${year}`,
    transform: function (body) {
      return cheerio.load(body);
    }
  }
  let $ = await rp(options)
  return $('table.wikitable.sortable tr:has(td)').map(function (i, elm) {
    if ($(this).find('th').length > 0) {
      let ranking = +$(this).find('th').text().trim()

      let artist_song = $(this).find('td').map(function (j, elm2) {
        return trim2($(this).text().trim(), '"')
      }).get()

      return {
        year: year,
        ranking: ranking,
        artist: artist_song[1],
        title: artist_song[0],
        lyrics: '',
        source: ''
      }
    } else {
      let artist_song = $(this).find('td').map(function (j, elm2) {
        return trim2($(this).text().trim(), '"')
      }).get()

      return {
        year: year,
        ranking: +artist_song[0],
        artist: artist_song[2],
        title: artist_song[1],
        lyrics: '',
        source: ''
      }
    }
  }).get()
}

async function scrape_all() {
  var promises = []

  for (var i = 1959; i <= 2018; i++) {
    promises.push(scrape(i))
  }

  Promise.all(promises)
    .then(results => {
      const fields = ['year', 'ranking', 'artist', 'title', 'lyrics', 'source'];
      const json2csvParser = new Json2csvParser({ fields });
      const csv = json2csvParser.parse(results.reduce((acc, val) => acc.concat(val), []));

      fs.writeFileSync('top_songs.csv', csv);
    })
}

scrape_all()
