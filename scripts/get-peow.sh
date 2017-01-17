#!/bin/bash
if [ ! -d "peow-cms" ]; then
	git clone https://github.com/the-sashko/peow-cms.git peow-cms
	cd peow-cms
	rm -rf .git
	chmod -x first-run.sh
	chmod 755 first-run.sh
	if [ "--ubuntu" == "$1" ] ; then
		./first-run.sh --ubuntu
	else
		./first-run.sh
	fi
	rm -f README.md
	rm -f LICENSE
	#rm -f ../get-peow.sh
else
	echo 'ERROR! DIRECTORY peow-cms ALREADY EXIST!'
fi
