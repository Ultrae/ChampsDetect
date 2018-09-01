#! /bin/sh

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

bad='data/train/bad/'
files=$(ls $bad)

for file in ${files}; do
  python reconnaissance.py $bad$file
done
