Interfaces
==========
There are several classes exposed. The primary one is the 
Key class. Note that strings are always converted to 
unicode. Regular strings (the str class) are used for binary 
buffers.

Key
===
The Key object wraps a registry key in a convenient way. It 
has several methods:
* akey.getPath(abbrev=True)
    Returns the path (eg, "HKCU\Software\Python 2.4") of the
    key wrapped by akey. If abbrev is False, the full root 
    (eg, HKEY_CURRENT_USER) is used.
* akey.flush()
    Calls _winreg.FlushKey(). See
    <http://msdn.microsoft.com/library/en-us/sysinfo/base/regflushkey.asp>
* akey.getMTime()
    Gets a datetime.datetime representing the time the key 
    was laste modified.
* akey.loadKey(key, file)
    Opposite of saveKey().
    Loads subkey key from file file. Only valid on 
    HKEY_LOCAL_MACHINE and HKEY_USERS.
* akey.saveKey(filename)
    Opposite of loadKey(). Saves the currrent key to file 
    filename.
* akey.openKey(key, sam=131097)
    Identical to akey.keys[key], except an error is 
    generated if the key does not exist. Also allows you to 
    specify permissions in sam. Use the KEY_* constants for 
    sam. See
    <http://msdn.microsoft.com/library/en-us/sysinfo/base/registry_key_security_and_access_rights.asp>
    for details.

The Key class also has several operators as shortcuts to 
using Key.values and Key.keys. They are:

* / - akey/sub
    Gets the subkey sub of akey. akey must be a Key object, sub must be a
    string.
* [] - akey[val]
    Returns a value of akey. val must be a string.
* in - childkey in akey
    Tests to see if childkey is a direct descendent of akey. childkey may be
    a Key instance or a string.

Key subclasses
==============
Key is subclassed to define the roots. Don't use the classes
directly, use these variables:
* HKEY_CLASSES_ROOT
* HKEY_CURRENT_CONFIG
* HKEY_CURRENT_USER
* HKEY_DYN_DATA
* HKEY_LOCAL_MACHINE
* HKEY_PERFORMANCE_DATA
* HKEY_USERS
Note that not all roots are usable on all versions of Windows. See
<http://msdn.microsoft.com/library/en-us/sysinfo/base/predefined_keys.asp> for 
details about them.