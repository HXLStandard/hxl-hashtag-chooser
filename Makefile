all: www/index.html

www/style.css: style.css
	mv style.css www

www/index.html: hxl-knowledge-base.json generate-tag-assist.py www/style.css
	python generate-tag-assist.py > www/index.html
