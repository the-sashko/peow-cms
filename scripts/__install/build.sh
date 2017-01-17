#!/bin/bash
project_path="$(pwd)/$(dirname $0)"
cd "${project_path/'/./'/'/'}"
curr_time=$(date '+%Y-%m-%d_%H-%M-%S')
zip -r tmp/$curr_time.zip build> /dev/null
cp tmp/$curr_time.zip back/$curr_time.zip
x=$(ls back | wc -l)
if [ $(ls back | wc -l) -gt 5 ]; then
	while [ $(ls back | wc -l) -gt 5 ]; do
		rm "back/$(ls -t back | tail -1)"
	done
fi
rm -rf build/*
./main.py
cp -r tmp/build/* build
rm -rf tmp/*
./scripts/send.sh