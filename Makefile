ifeq ($(shell uname),)
  PYTHON=python
else
  PYTHON=wine python
endif

VER=$(shell $(PYTHON) setup.py -V)
DIST=dist/pyreg-$(VER).win32.zip dist/pyreg-$(VER).win32.exe
README=src/README.txt

dist : $(DIST)

all : $(DIST) test upload register

register : upload $(DIST)
	$(PYTHON) setup.py register
	
test : src/* install
	$(PYTHON) src\\tests\\smoke.py

dist/pyreg-${VER}.win32.zip : src/*
	$(PYTHON) setup.py bdist --format=zip

dist/pyreg-${VER}.win32.exe : src/*
	$(PYTHON) setup.py bdist_wininst

clean :
	$(PYTHON) setup.py clean

install : 
	$(PYTHON) setup.py install
.PHONY : all register upload test clean dist

include upload.mk
