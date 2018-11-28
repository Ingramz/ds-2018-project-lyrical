#!/usr/bin/env bash
filename="csvs/lyrics.csv"
total_lines=$(wc -l <${filename})
((lines_per_file = (total_lines + 4) / 5))
mkdir lx
split --lines=${lines_per_file} ${filename} lx/

for file in lx/*; do
    (
        while read line; do
            if grep -qP --color=auto '^[0-9]+,.*?,[0-9]{3,4},.*?,.*?,"' <<< "$line"; then
                echo $line | tr '\n' ' ' | sed -e 's/^/\n/' >> ${file}.out;
            else
                echo $line | tr '\n' ' ' >> ${file}.out;
            fi
        done < $file
    ) &
done
wait

cat lx/*.out > newline_cleaned_lyrics.csv
rm -rf lx`


