const Papa = require('papaparse')
const fs = require('fs')
var Iconv  = require('iconv').Iconv;
var iconv = new Iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE');
const Json2csvParser = require('json2csv').Parser;

let data = []

fs.readdirSync('Data/Lyrics-Clean').forEach(file => {
  console.log(file)

  rows = Papa.parse(fs.readFileSync('Data/Lyrics-Clean/' + file, 'UTF-8').trim(), {
    delimiter: ',',
    header: true}
  ).data.forEach(row => data.push(row))
})

fs.writeFileSync('Data/all-songs.csv', Papa.unparse(data))
