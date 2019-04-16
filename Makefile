all: docs/index.html

docs/style.css: style.css
	cp style.css docs/style.css

docs/script.js: script.js
	cp script.js docs/script.js

docs/icon.png: icon.png
	cp icon.png docs/icon.png

docs/manifest.appcache: manifest.appcache
	cp manifest.appcache docs/manifest.appcache

docs/index.html: hxl-knowledge-base.json gen-chooser.py docs/style.css docs/script.js docs/icon.png docs/manifest.appcache
	python gen-chooser.py > docs/index.html || rm docs/index.html
