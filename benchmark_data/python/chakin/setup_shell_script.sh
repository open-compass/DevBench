#!/bin/sh

sudo apt-get install build-essential libatlas-base-dev
pip install --upgrade pip setuptools
pip install --upgrade pip setuptools wheel
pip install --use-pep517 -r requirements.txt
