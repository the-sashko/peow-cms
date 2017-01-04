#!/bin/bash
if [ "--ubuntu" == "$1" ] ; then
	./scripts/install.sh --ubuntu
else
	./scripts/install.sh
fi