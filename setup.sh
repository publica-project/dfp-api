#!/usr/bin/env bash

if [[ "$(uname)" == "Darwin" ]]; then
	if [[ "$(command -v python)" == "" ]]; then
		echo "installing python2"
		echo "================================================================"
		brew install python2
	fi
fi

if [[ "$(command -v pip)" == "" ]]; then
	echo "installing pip"
	echo "================================================================"
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	python get-pip.py
fi

if [[ "$(pip show virtualenv)" == "" ]]; then
	echo "installing virtualenv"
	echo "================================================================"
	pip install virtualenv
fi

if [[ ! -d ".env" ]]; then
	echo "setup virtualenv"
	echo "================================================================"
	virtualenv .env
fi

source .env/bin/activate

exec_req=
while read line; do
	if [[ "$(pip show "${line}")" == "" ]]; then
		exec_req=true
		break
	fi
done < './requirements.txt'

if [[ "${exec_req}" != "" ]]; then
	echo "installing new python modules"
	echo "================================================================"
	pip install -r requirements.txt
fi
