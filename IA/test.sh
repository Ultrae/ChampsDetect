#! /bin/sh


bad='data/train/bad/'
files=$(ls $bad)

for file in ${files}; do
  python reconnaissance.py $bad$file
done
