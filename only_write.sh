#!/bin/sh

cp ./plugins/status-log.py.es ./plugins/status-log.py
cd ./es
LANG=es_ES.utf8 rawdog -c config.es -w -d .

cd ..

cp ./plugins/status-log.py.en ./plugins/status-log.py
cd ./en
LANG=en_GB.utf8 rawdog -c config.en -w -d .

