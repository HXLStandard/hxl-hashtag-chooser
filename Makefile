# activation script for the Python virtual environment
VENV=venv/bin/activate

all: docs/en/index.html docs/fr/index.html

view: docs/en/index.html docs/fr/index.html
	firefox docs/en/index.html docs/fr/index.html

validate: $(VENV)
	. $(VENV) && python validate-base.py

docs/style.css: style.css
	cp style.css docs/style.css

docs/script.js: script.js
	cp script.js docs/script.js

docs/icon.png: icon.png
	cp icon.png docs/icon.png

docs/en/index.html: $(VENV) validate hxl-knowledge-base.json gen-chooser.py docs/style.css docs/script.js docs/icon.png
	. $(VENV) && mkdir -p docs/en && python gen-chooser.py en > $@ || rm -f $@

docs/fr/index.html: $(VENV) validate hxl-knowledge-base.json gen-chooser.py docs/style.css docs/script.js docs/icon.png
	. $(VENV) && mkdir -p docs/fr && python gen-chooser.py fr > $@ || rm -f $@

clean:
	rm -rf venv docs/en docs/fr

# (re)build the virtual environment if it's missing, or whenever setup.py changes
# requires that Python3 virtualenv package be installed
$(VENV): requirements.txt
	rm -rf venv && virtualenv venv && . $(VENV) && pip install -r requirements.txt

