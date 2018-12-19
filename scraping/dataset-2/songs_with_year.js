const Papa = require('papaparse')
const fs = require('fs')
var Iconv  = require('iconv').Iconv;
var iconv = new Iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE');
const Json2csvParser = require('json2csv').Parser;

let data = []
let n_rows = 0
let n_with_year = 0

fs.readdirSync('Data/Lyrics-Clean').forEach(file => {
  console.log(file)

  rows = Papa.parse(fs.readFileSync('Data/Lyrics-Clean/' + file, 'UTF-8').trim(), {
    delimiter: ',',
    header: true}
  ).data

  for (let row of rows) {
    if (+row.Year) {
      data.push(row)
      n_with_year++
    }
    n_rows++
  }
})

console.log(n_with_year + ' / ' + n_rows)

fs.writeFileSync('Data/songs-with-year.csv', Papa.unparse(data, {header: true}))
