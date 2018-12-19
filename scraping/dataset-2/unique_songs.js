const Papa = require('papaparse')
const fs = require('fs')
var Iconv  = require('iconv').Iconv;
var iconv = new Iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE');
const Json2csvParser = require('json2csv').Parser;
var HashMap = require('hashmap');

var uniques = {}
var data = []

fs.readdirSync('Data/Lyrics-Clean').forEach(file => {
  console.log(file)

  rows = Papa.parse(fs.readFileSync('Data/Lyrics-Clean/' + file, 'UTF-8').trim(), {
    delimiter: ',',
    header: true}
  ).data

  for (let row of rows) {
    if (!uniques[row.Lyrics]) {
      data.push(row)
      uniques[row.Lyrics] = true
    }
  }
})

fs.writeFileSync('Data/songs-unique.csv', Papa.unparse(data, {header: true}))
