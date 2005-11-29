@echo off

set VER=%1

python setup.py sdist

echo open endeavour.zapto.org > pyreg-up.txt
echo astro73 >> pyreg-up.txt
echo tbonerox >> pyreg-up.txt
echo cd astro73/pyreg >> pyreg-up.txt
echo binary >> pyreg-up.txt
echo put dist\pyreg-%VER%.zip >> pyreg-up.txt
echo bye >> pyreg-up.txt

:: %SYSTEMROOT%\system32\ftp -s:pyreg-up.txt -i

:: python setup.py register
