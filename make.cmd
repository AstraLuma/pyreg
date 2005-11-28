@echo off

set VER=%1

python setup.py sdist

ftp -s:pyreg-up.txt -i

python setup.py register
