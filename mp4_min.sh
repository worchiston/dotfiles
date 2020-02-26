#!/bin/bash
# Optimises all .mp4 files in a directory -> smaller file size

if [ $# -eq 0 ]; then
    echo 'usage: ./mp4_min [directory]'
    exit
fi

for i in $1*.mp4
do
    ffmpeg -loglevel 0 -i "$i" -vcodec libx265 -crf 20 "${i%.*}_MIN.mp4"
    echo "Done ... $i"
done
