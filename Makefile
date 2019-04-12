all: docs/index.html

docs/style.css: style.css
	cp style.css docs/style.css

docs/script.js: script.js
	cp script.js docs/script.js

docs/index.html: hxl-knowledge-base.json gen-chooser.py docs/style.css docs/script.js
	python gen-chooser.py > docs/index.html
