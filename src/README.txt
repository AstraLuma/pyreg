First of all, _winreg should die. It has no respect whatsoever of data types.
Here's why:
* REG_DWORD, REG_DWORD_LITTLE_ENDIAN - Returns a signed int, not an unsigned 
  long
* REG_DWORD_BIG_ENDIAN - Returns a binary str buffer of size 4, not an unsigned 
  long
* REG_LINK - Returns a binary str containing raw UCS-2, not an unicode

Overview
========

Notes:
* Registry paths are normalized to backslashes

Modules
=======
There are several modules defined by pyreg:
* pyreg - basic, imports all of the others
* pyreg.key - defines the base Key class
* pyreg.types - defines type classes used to wrap the registry's types
* pyreg.roots - defines HKEY_CURRENT_USER et al

Note that strings are always converted to unicode. Regular strings (the str 
class) are used for binary buffers.

pyreg.key
=========

Key
---
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
* akey.getParent()
    Returns the true parent (ie, not necesarily the key used to create it) of 
    akey.

The Key class also has several operators as shortcuts to 
using Key.values and Key.keys. They are:

* / - akey/sub
    Gets the subkey sub of akey. akey must be a Key object, sub must be a
    string (str or unicode).
* | - akey|val
    Gets the value val of akey. akey must be a Key instance, val must be a 
    string (str or unicode).
* [] - akey[val]
    Returns a value of akey. val must be a string.
* in - childkey in akey
    Tests to see if childkey is a direct descendent of akey. childkey may be
    a Key instance or a string. This is not recursive.

Key.keys
--------
The Key.keys object is accessable only from a Key instance. It should never
be created seperate from a Key.

Key.keys is a dictionary of the subkeys of its creator Key. Therefore, all its
items are also Key instances.

Key.keys supports all the methods of a dictionary, although many are 
inefficient.

If a non-existant key is accessed, a new one is created.

(Technical note: Key.keys is of the class _RegKeys which should not be 
instanciated manually. _RegKeys extends UserDict.DictMixin, so is not a 
pre-gnerated dict, rather it calls the _winreg functions to get values and 
such.)

Key.values
----------
Much like Key.keys, except it is for the values of its parent key. All its 
items are of one of the classes in pyreg.types. It supports all methods of a 
dictionary, although some are inefficient.

When an non-existant value is accessed, Key.values raises a KeyError exception.

(Technical note: Like Key.keys, Key.values is of the class _RegValues, 
which is, again, a subclass of UserDict.DictMixin. Follow the same rules as 
with Key.keys.)

ValueReference
--------------
This allows you to refer to a value without actually getting the value. It is
obtained either by calling Key.values.ref() with the value name, or by creating
it yourself and passing it the Key and value.

Note that there is no equivelent for keys, since all their data is generated
anyway.

Operators (aref refers to a ValueReference instance):
* () - aref()
    Gets the value (dereferences) of this value. Meaning it calls the original 
    key and gets the value.

pyreg.roots
===========
Key is subclassed to define the registry's roots. Don't use the classes 
directly, use these variables instead:
* HKEY_CLASSES_ROOT
* HKEY_CURRENT_CONFIG
* HKEY_CURRENT_USER
* HKEY_DYN_DATA
* HKEY_LOCAL_MACHINE
* HKEY_PERFORMANCE_DATA
* HKEY_PERFORMANCE_NLSTEXT
* HKEY_PERFORMANCE_TEXT
* HKEY_USERS
Note that not all roots are usable on all versions of Windows. See
<http://msdn.microsoft.com/library/en-us/sysinfo/base/predefined_keys.asp> for 
details about them.

***WARNING***
HKEY_PERFORMANCE_NLSTEXT and HKEY_PERFORMANCE_TEXT only contain a few 
values of the type REG_MULTI_SZ. However, the number of items within those 
values numbers in the thousands. Use caution when enumerating.

pyreg.types
===========
To wrap the registry's types, several classes were written. pyreg.types also 
handles demunging data.

(Note: Each class name is followed by the REG_* constant it wraps.)

Binary - REG_BINARY
------
Behaves similarly to str. In fact, it is a subclass of str that does not define
any methods.

DWORD - REG_DWORD
-----
A long, other than that it is limited to the range of an unsigned 32-bit value.

DWORD_LittleEndian - REG_DWORD_LITTLE_ENDIAN
------------------
Identical to DWORD (because Windows is a little-endian system).

DWORD_BigEndian - REG_DWORD_BIG_ENDIAN
---------------
Basically the same as a DWORD, except that it is stored in big endian form in 
the registry. (It appears in the correct order to scripts.)

ExpandingString - REG_EXPAND_SZ
---------------
A unicode string that contains enviroment variables (%foo%).

Link - REG_LINK
----
Note: "Applications should not use this type." (MSDN)

A unicode string.

MultiString - REG_MULTI_SZ
-----------
A list of unicode strings. It will only deal with types that can be converted to
a string.

rNone - REG_NONE
-----
A value of no defined type; behaves identically to Binary.

ResourceList - REG_RESOURCE_LIST
------------
If you know details about this data type, I would like to hear about it. Until
then, it behaves like Binary.

String - REG_SZ
------
A unicode string. (Strings are always Unicode due to _winreg implementation, 
although if this changes, I am likely to force unicode anyway.)

About data type conversion
--------------------------
During the save and load processes, data types are converted to/from a form that
_winreg will store correctly, aka (de)munging). You may define your own 
classes that pyreg can store by either:
* Inheriting from one of the pre-defined types above
* Defining the __to_registry__ function

You may also allow your class to be created upon retrieval. To do this, you 
must:
1. Define __from_registry__ as a class-callable type (ie, staticmethod or 
   classmethod), which returns an instance of your class
2. Add your type to the pyreg.types._registryDataClasses dictionary, the key 
   being the type constant used by _winreg

Note that if you inherit from a native type already handled, and can accept 
registry data in your constructor, you may inherit from RegistryType as well.

$Date$
