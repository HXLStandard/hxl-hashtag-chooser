# activation script for the Python virtual environment
VENV=venv/bin/activate

all: docs/index.html

view: docs/index.html
	firefox $<

validate: $(VENV)
	. $(VENV) && python validate-base.py

docs/style.css: style.css
	cp style.css docs/style.css

docs/script.js: script.js
	cp script.js docs/script.js

docs/icon.png: icon.png
	cp icon.png docs/icon.png

docs/index.html: $(VENV) validate hxl-knowledge-base.json gen-chooser.py docs/style.css docs/script.js docs/icon.png
	. $(VENV) && python gen-chooser.py > docs/index.html || rm docs/index.html

# (re)build the virtual environment if it's missing, or whenever setup.py changes
# requires that Python3 virtualenv package be installed
$(VENV): requirements.txt
	rm -rf venv && virtualenv venv && . $(VENV) && pip install -r requirements.txt

