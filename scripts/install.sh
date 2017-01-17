#!/bin/bash
if [ "--ubuntu" == "$1" ] ; then
	./scripts/__install/ubuntu.sh
fi
virtualenv -p python3 peowenv
source peowenv/bin/activate
sudo pip3 install markdown2
sudo pip3 install transliterate
sudo pip3 install pillow
deactivate
cp ./scripts/__install/build.sh build.sh
chmod -x build.sh
chmod 755 build.sh
chmod -x main.py
chmod 755 main.py
mkdir back
chmod -R 755 back
mkdir build
chmod -R 755 build
mkdir tmp
chmod -R 755 tmp
mkdir content
chmod -R 755 content
cp -r ./scripts/__install/demo/* content
rm -f first-run.sh