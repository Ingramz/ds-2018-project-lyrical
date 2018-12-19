const Papa = require('papaparse')
const fs = require('fs')
var Iconv  = require('iconv').Iconv;
var iconv = new Iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE');
const Json2csvParser = require('json2csv').Parser;
var HashMap = require('hashmap');

var uniques = {}

function bump(lyrics) {
  let result = 0
  let hash = lyrics.map(x => {
    let nx = uniques.get(x)
    if (nx) {
      return nx
    }
    unique_n++
    uniques.set(x, unique_n)
    return unique_n
  }).reduce((acc, curval) => curval * 65536 + acc)

  ngrams.set(hash, (ngrams.get(hash) || 0) + 1)
}

rows = Papa.parse(fs.readFileSync('Data/songs-unique.csv', 'UTF-8').trim(), {
  delimiter: ',',
  header: true}
).data

for (let row of rows) {
  if (row.Lyrics.indexOf('in the night') !== -1) {
    console.log(row.Band, row.Song, row.Year)
  }
}

console.log("done")

// var sortable = [];
// for (var vehicle in uniques) {
//     sortable.push([vehicle, uniques[vehicle]]);
// }
//
// sortable.sort(function(a, b) {
//     return b[1] - a[1];
// });
//
// console.log(sortable.slice(0, 19))
