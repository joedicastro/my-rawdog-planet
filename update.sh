#!/bin/sh

cp ./plugins/status-log.py.es ./plugins/status-log.py
cd ./es
LANG=es_ES.utf8 rawdog -c config.es -uw -d .

cd ..

cp ./plugins/status-log.py.en ./plugins/status-log.py
cd ./en
LANG=en_GB.utf8 rawdog -c config.en -uw -d .

