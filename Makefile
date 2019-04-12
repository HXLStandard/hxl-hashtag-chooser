all: docs/index.html

docs/style.css: style.css
	cp style.css docs/style.css

docs/index.html: hxl-knowledge-base.json gen-chooser.py docs/style.css
	python gen-chooser.py > docs/index.html
