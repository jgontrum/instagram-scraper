#!/bin/bash

cd /app
python -m http.server "$PORT" &
env/bin/scrapy crawl --loglevel=INFO instagram