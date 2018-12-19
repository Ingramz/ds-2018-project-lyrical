const Papa = require('papaparse')
const fs = require('fs')
var Iconv  = require('iconv').Iconv;
var iconv = new Iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE');
const Json2csvParser = require('json2csv').Parser;

fs.readdirSync('Data/Lyrics').forEach(file => {
  console.log(file)

  data = Papa.parse(fs.readFileSync('Data/Lyrics/' + file, 'UTF-8').trim(), {
    delimiter: ',',
    header: true}
  ).data

  for (let row of data) {
    row.Lyrics = iconv.convert(row.Lyrics.normalize('NFKD'))
      .toString()
      .toLowerCase()
      .replace(/[=+)(*&^%$#@!~?;\":><,./\r\n\-]|\[.*?\]/g, ' ')
      .replace(/\s+/g, ' ')
      .replace(/['`]/g, '')
      .trim()
  }

  const fields = ['Band', 'Lyrics', 'Song', 'Year']
  const json2csvParser = new Json2csvParser({ fields })
  const csv = json2csvParser.parse(data)

  fs.writeFileSync('Data/Lyrics-Clean/' + file, csv)
})
