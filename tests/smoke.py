"""
smoke test for pyreg.
"""
print "Welcome to the pyreg smoketest suite!"
print "If any errors appear, please investigate and"
print "report them to <astronouth7303@gmail.com>."
import sys
def pause(text=''):
    """Waits for input from STDIN."""
    print text
    if sys.stdin.isatty():
        sys.stdin.flush()
        c = None
        while c is None: c = sys.stdin.read(1)

print "Begin basic tests."
print "Before import: ",dir()
from pyreg import *
print "After: ",dir()
print ""
print "The roots:"
import pyreg.roots
print pyreg.roots.HKEY_CLASSES_ROOT
print pyreg.roots.HKEY_CURRENT_CONFIG
print pyreg.roots.HKEY_CURRENT_USER
print pyreg.roots.HKEY_DYN_DATA
print pyreg.roots.HKEY_LOCAL_MACHINE
print pyreg.roots.HKEY_PERFORMANCE_DATA
print pyreg.roots.HKEY_USERS
print ""
print "ok, enough of that."
pause('')

target = HKEY_CURRENT_USER
print "Subkeys in "+str(target)+":"
for k in target.keys:
    print " *",k
pause()

print "Arbitrarily pull up a key:"
target = HKEY_CURRENT_USER/'Software'/'Microsoft'/'Windows'/'CurrentVersion'/'Internet Settings'
print " code: HKEY_CURRENT_USER/'Software'/'Microsoft'/'Windows'/'CurrentVersion'/'Internet Settings'"
print " result:",repr(target)
pause()

print "Values in "+str(target)+":"
for v in target.values:
    print " *",v
pause()    
print "And with their content:"
for v in target.values:
    print " *",v
    print "\t",target[v].__class__.__name__,"-",target[v]
pause()

type_values = {
    'bin' : Binary("\x12\x34\x56\x78\x90"),
    'dword' : DWORD(0x12345678),
    'bdword' : DWORD_BigEndian(0x12345678),
    'ldword' : DWORD_LittleEndian(0x12345678),
    'estr' : ExpandingString('You are %USER%'),
    'link' : Link(u'some link?'),
    'mstr' : MultiString(['this','is','a','MultiString.','Each','word','is','a','new','string.']),
    'none' : rNone('blahdy blah \xDE\xAD\xBE\xEF'),
    'rlist' : ResourceList('What is this?'),
    'str' : String("A plain ol' string")
    }

if 'test' in HKEY_CURRENT_USER:
    print "Hey! You've done this before!"
    print ""
    target = HKEY_CURRENT_USER.keys['test']
    print "The Types Test Suite, Part I: Reading"
    print "I will show you each of the values in",target,"and their content."
    print "You are to report errors that appear."
    print "If any of the values do not match, try again before reporting the error."
    print "Ready? Begin."
    for v in target.values:
        print " *",v
        print "\t",target.values[v].__class__.__name__,"-",target[v]
        if target[v] != type_values[v.lower()]: print "\tDoes not match stored value!"
else:
    print "Skipping The Types Test Suite, Part I: Reading"
    print "Run this script again to perform Part I."

pause()

target = HKEY_CURRENT_USER.keys['test']
print "The Types Test Suite, Part II: Writting"
print "I will write predefined values in to",target,"."
print "You are to report errors that appear."
from time import *
n = int(time())
print "Ready? Begin."
for v in type_values:
    if n & 1:
        print v,"(k[v])"
        target[v] = type_values[v]
    else:
        print v,"(k.values[v])"
        target.values[v] = type_values[v]
    n += 1

pause()
print "Good-bye!"
