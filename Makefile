all: www/index.html

www/style.css: style.css
	cp style.css www

www/index.html: hxl-knowledge-base.json gen-chooser.py www/style.css
	python gen-chooser.py > www/index.html
