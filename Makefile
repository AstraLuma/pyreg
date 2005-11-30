VER=${shell python setup.py -V}
DIST=dist/pyreg-${VER}.win32.zip dist/pyreg-${VER}.win32.exe
README=src/README.txt

.PHONY : register upload

all : ${DIST} upload register

register : upload ${DIST}
	python setup.py register

dist/pyreg-${VER}.win32.zip : src/*
	python setup.py bdist --format=zip

dist/pyreg-${VER}.win32.exe : src/*
	python setup.py bdist_wininst

upload : ${DIST} ${README}
	scp -v ${DIST} ${README} "Astronouth7303@endeavour.zapto.org:/cygdrive/e/var/htdocs/endeavour/astro73/pyreg"
	
clean :
	python setup.py clean

install : 
	python setup.py install
