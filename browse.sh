#!/bin/sh

python -m SimpleHTTPServer &

sensible-browser http://localhost:8000/planet/es
