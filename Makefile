ifeq ($(shell uname),)
  PYTHON=python
else
  PYTHON=wine python
endif

VER=$(shell $(PYTHON) setup.py -V)
BDIST=dist/pyreg-$(VER).win32.zip dist/pyreg-$(VER).win32.exe
SDIST=dist/pyreg-$(VER).zip
README=README.txt

SOURCES=$(wildcard src/*.py src/pyreg/*.py src/pyreg/test/*.py)

dist : bdist sdist

bdist : $(BDIST)

sdist : $(SDIST)

all : $(BDIST) test upload register

register : upload $(BDIST)
	$(PYTHON) setup.py register

test : $(SOURCES) install
	$(PYTHON) src\\tests\\smoke.py

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
.PHONY : all register upload test clean dist sdist bdist

include upload.mk
