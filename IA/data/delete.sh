#! /bin/sh

files=$(ls)
for file in $files; do
  dataR=$(($RANDOM % 100))
  [ $dataR -gt 90 ] && echo $file
done
