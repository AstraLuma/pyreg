VER=${shell python setup.py -V}
DIST=dist/pyreg-${VER}.win32.zip dist/pyreg-${VER}.win32.exe
README=src/README.txt

.PHONY : register upload test

all : ${DIST} test upload register

register : upload ${DIST}
	python setup.py register
	
test : src/* install
	python src\\tests\\smoke.py

dist/pyreg-${VER}.win32.zip : src/*
	python setup.py bdist --format=zip

dist/pyreg-${VER}.win32.exe : src/* test
	python setup.py bdist_wininst

upload : ${DIST} ${README} test
	scp -v ${DIST} ${README} "Astronouth7303@endeavour.zapto.org:/cygdrive/e/var/htdocs/endeavour/astro73/pyreg"
	
clean :
	python setup.py clean

install : 
	python setup.py install
