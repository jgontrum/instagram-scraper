.PHONY: clean start test crawl crawl-proxy

TAG=$(shell git symbolic-ref -q --short HEAD)
PIPOPTIONS=--default-timeout=100

# Set a specific path for the Python executable if anaconda is the primary
# distribution on your system.
# PYTHON3=python3.6
PYTHON3=/usr/local/Cellar/python3/3.6.1/Frameworks/Python.framework/Versions/3.6/bin/python3.6

all: env/bin/python

env/bin/python:
	$(PYTHON3) -m venv env
	touch requirements.txt
	env/bin/pip install $(PIPOPTIONS) --upgrade pip
	env/bin/pip install $(PIPOPTIONS) wheel
	env/bin/pip install $(PIPOPTIONS) -r requirements.txt

crawl: env/bin/python
	env/bin/scrapy crawl --loglevel=INFO Wikia.com

clean:
	rm -rfv bin develop-eggs dist downloads eggs env parts .cache .scannerwork
	rm -fv .DS_Store .coverage .installed.cfg bootstrap.py .coverage
	find . -name '*.pyc' -exec rm -fv {} \;
	find . -name '*.pyo' -exec rm -fv {} \;
	find . -depth -name '*.egg-info' -exec rm -rfv {} \;
	find . -depth -name '__pycache__' -exec rm -rfv {} \;
