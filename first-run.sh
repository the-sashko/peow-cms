#!/bin/bash
if [ "--ubuntu" == "$1" ] ; then
	./tools/install.sh --ubuntu
else
	./tools/install.sh
fi
./tools/configurator.py