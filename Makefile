ifeq ($(shell uname),)
  PYTHON=python
else
#WINEDEBUG=fixme-all 
  PYTHON=wine python
endif

VER:=$(shell $(PYTHON) setup.py -V)
BDIST=dist/pyreg-$(VER).win32.zip dist/pyreg-$(VER).win32.exe
SDIST=dist/pyreg-$(VER).zip
README=README.txt readme.html

SOURCES=$(wildcard src/*.py src/pyreg/*.py src/pyreg/test/*.py)

dist : bdist sdist

bdist : $(BDIST)

sdist : $(SDIST)

release : dist test upload register
	svn ps --non-interactive svn:needs-lock "*" $(BDIST) $(SDIST)

register : upload $(BDIST)
	python setup.py register

test : $(SOURCES) install
	$(PYTHON) tests\\smoke.py

dist/pyreg-${VER}.win32.zip : $(SOURCES)
	$(PYTHON) setup.py bdist --format=zip

dist/pyreg-${VER}.zip : $(SOURCES) setup.py MANIFEST.in README.txt Makefile
	$(PYTHON) setup.py sdist

dist/pyreg-${VER}.win32.exe : $(SOURCES)
	$(PYTHON) setup.py bdist_wininst

clean :
	$(PYTHON) setup.py clean

install : 
	$(PYTHON) setup.py install
.PHONY : release register upload test clean dist sdist bdist

include upload.mk
