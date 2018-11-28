#!/usr/bin/env bash

filename='csvs/songdata.csv'
output_filename='newline_cleaned_songdata.csv'
echo "Processing $filename"
total_lines=$(wc -l <${filename})
echo "Lines in $filename: $total_lines"
procs=$(nproc)
((lines_per_file = (total_lines + procs - 1) / procs))
echo "Splitting file in $procs and placing in temporary folder for processing..."
mkdir sd
split --lines=${lines_per_file} ${filename} sd/

for file in sd/*; do
    (
        echo "processing $file"
        while read line; do
            line=$(echo "$line" | tr '[:upper:]' '[:lower:]' | perl -pe 's/[[(].*?chorus.*?[])]//g;' -pe 's/\[.*?\]//g;')
            if grep -qP --color=auto '^.*?,.*?,.*?\.html,"' <<< "$line"; then
                echo $line | tr '\n' ' ' | sed -e 's/^/\n/' >> ${file}.out;
            else
                echo $line | tr '\n' ' ' >> ${file}.out
            fi
        done <<< $(head -2000 $file)
        echo "$file done"
    ) &
done
wait

echo "all files done: merging files together..."
cat sd/*.out > $output_filename
echo "deleting temporary folder"
rm -rf sd




