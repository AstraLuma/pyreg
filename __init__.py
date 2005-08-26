"""Defines classes to interface with the registry via _winreg.

Interfaces
==========
There are several classes exposed. The primary one is the Key class. Note that
strings are always converted to unicode. Regular strings (str class) are used
for binary buffers.

The Key Class
-------------
The Key object wraps a registry key in a convenient way. It has several methods:
* akey.getPath(abbrev=True)
    Returns the path (eg, "HKCU\Software\Python 2.4") of the key
    wrapped by akey. If abbrev is False, the full root (eg, HKEY_CURRENT_USER)
    is used.
* akey.flush()
    Calls _winreg.FlushKey(). See
    <http://msdn.microsoft.com/library/en-us/sysinfo/base/regflushkey.asp>
* akey.getMTime()
    Gets a datetime.datetime representing the time the key was laste modified.
* akey.loadKey(key, file)
    Opposite of saveKey().
    Loads subkey key from file file. Only valid on HKEY_LOCAL_MACHINE and
    HKEY_USERS.
* akey.saveKey(filename)
    Opposite of loadKey(). Saves the currrent key to file filename.
* akey.openKey(key, sam=131097)
    Identical to akey.keys[key], except an error is generated if the
    key does not exist. Also allows you to specify permissions in sam.
    Use the KEY_* constants for sam. See
    <http://msdn.microsoft.com/library/en-us/sysinfo/base/registry_key_security_and_access_rights.asp>
    for details.

The Key class also has several operators as shortcuts to using Key.values and
Key.keys.

* / - akey/sub
    Gets the subkey sub of akey. akey must be a Key object, sub must be a
    string.
* [] - akey[val]
    Returns a value of akey. val must be a string.
* in - childkey in akey
    Tests to see if childkey is a direct descendent of akey. childkey may be
    a Key instance or a string.

Key subclasses
=============
"""
import _winreg as winreg
import datetime
from datetime import timedelta, date, time, datetime
import sys
from types import *
from UserDict import DictMixin

class pyregException(Exception):
	"""An error occuried in the pyreg module."""
class pyregWarning(RuntimeWarning, UserWarning):
	"""A warning occuried in the pyreg module."""
	
class HKEYWrongOSVersion(pyregException):
	"""The requested predefined key is not available in this version of Windows."""
	key = 0

class Binary(str):
	"""MSDN: "Binary data in any form."
	
	Encapsulates the REG_BINARY type; based on str."""
	pass

class DWORD(long):
	"""MSDN: "A 32-bit number."
	
	Encapsulates the REG_DWORD type.
	Exactly like long, except it is limited to 0-0xFFFFFFFF."""
	def __new__(cls, x, base=False):
		if(base is False):
			inst = super(DWORD, cls).__new__(cls, x)
		else:
			inst = super(DWORD, cls).__new__(cls, x, base)
		if (inst < 0 or inst > 0xFFFFFFFF):
			raise OverflowError
		return inst

class DWORD_LittleEndian(DWORD):
	"""MSDN: "A 32-bit number in little-endian format. This is equivalent to REG_DWORD.
	In little-endian format, a multi-byte value is stored in memory from the lowest byte (the "little end") to the highest byte. For example, the value 0x12345678 is stored as (0x78 0x56 0x34 0x12) in little-endian format.
	Windows NT/Windows 2000, Windows 95, and Windows 98 are designed to run on little-endian computer architectures. A user may connect to computers that have big-endian architectures, such as some UNIX systems."
	
	Encapsulates REG_DWORD_LITTLE_ENDIAN; identical to DWORD"""
	pass

class DWORD_BigEndian(Binary):
	"""MSDN: "A 32-bit number in big-endian format.
	In big-endian format, a multi-byte value is stored in memory from the highest byte (the "big end") to the lowest byte. For example, the value 0x12345678 is stored as (0x12 0x34 0x56 0x78) in big-endian format."

	Encapsulates REG_DWORD_BIG_ENDIAN, behaves like Binary."""
	pass

class ExpandingString(unicode):
	"""MDSN: "A null-terminated string that contains unexpanded references to environment variables (for example, "%PATH%"). It will be a Unicode or ANSI string depending on whether you use the Unicode or ANSI functions. To expand the environment variable references, use the ExpandEnvironmentStrings function."

	Encapsulates REG_EXPAND_SZ, based on unicode."""
	pass


class Link(unicode):
	"""MSDN: "A Unicode symbolic link. Used internally; applications should not use this type."
	
	Encapsulates REG_LINK, based on unicode."""
	pass

class MultiString(list):
	"""MSDN: "An array of null-terminated strings, terminated by two null characters."

	Encapsulates REG_MULTI_SZ; based on list.
	Make sure you only pass strings to it, it will raise a TypeError otherwise."""
	def __init__(self,seq=False):
		if seq is not False:
			list.__init__(self, seq)
			for i in self:
				if not isinstance(i, basestring): raise TypeError
		else:
			list.__init__(self)
	def __setitem__(self, key, value):
		if isinstance(key, slice):
			for i in value:
				if not isinstance(i, basestring): raise TypeError
		else:
			if not isinstance(value, basestring): raise TypeError
		list.__setitem__(self, key, value)
	def __setslice__(self, i, j, sequence):
		for i in sequence:
			if not isinstance(i, basestring): raise TypeError
		list.__setslice__(self, i, j, sequence)
	def append(self,x):
		if (isinstance(x, basestring)): raise TypeError
		list.append(self,x)

class rNone(Binary):
	"""MSDN: "No defined value type."

	Wraps REG_NONE, same as Binary."""
	pass

class ResourceList(Binary):
	"""MSDN: "A device-driver resource list."

	Encapsulates REG_RESOURCE_LIST; behaves like Binary."""

class String(unicode):
	"""MDSN: "A null-terminated string. It will be a Unicode or ANSI string, depending on whether you use the Unicode or ANSI functions."

	Encapsulates REG_SZ, based on unicode. (strings are always Unicode due to _winreg implementation.)"""
	pass

def _Registry2Object(t,v):
	"""Converts the given object and registry type to a registry type object."""
	if t == winreg.REG_BINARY:
		return Binary(v)
	elif t == winreg.REG_DWORD:
		return DWORD(v)
	elif t == winreg.REG_DWORD_LITTLE_ENDIAN:
		return DWORD_LittleEndian(v)
	elif t == winreg.REG_DWORD_BIG_ENDIAN:
		return DWORD_BigEndian(v)
	elif t == winreg.REG_EXPAND_SZ:
		return ExpandingString(v)
	elif t == winreg.REG_LINK:
		return Link(v)
	elif t == winreg.REG_MULTI_SZ:
		return MultiString(v)
	elif t == winreg.REG_NONE:
		return rNone(v)
	elif t == winreg.REG_RESOURCE_LIST:
		return ResourceList(v)
	elif t == winreg.REG_SZ:
		return String(v)
	else:
		# Assume REG_NONE
		return rNone(v)

def _Object2Registry(v):
	"""Converts the given registry type object to a tuple containing a winreg-compatible object and a type.
	You can also pass some native types, as follows:
	+ basestring\t->\tREG_SZ
	+ list, tuple, set, enumerate, frozenset, generator, xrange\t->\tREG_MULTI_SZ
	+ buffer\t->\tREG_BINARY"""
	#We avoid inheritance problems by checking them in the reverse order they were defined
	if isinstance(v, String):
		return (v, winreg.REG_SZ)
	elif isinstance(v, ResourceList):
		return (v, winreg.REG_RESOURCE_LIST)
	elif isinstance(v, rNone):
		return (v, winreg.REG_NONE)
	elif isinstance(v, MultiString):
		return (v, winreg.REG_MULTI_SZ)
	elif isinstance(v, Link):
		return (v, winreg.REG_LINK)
	elif isinstance(v, ExpandingString):
		return (v,winreg.REG_EXPAND_SZ)
	elif isinstance(v, DWORD_BigEndian):
		return (v, winreg.REG_DWORD_BIG_ENDIAN)
	elif isinstance(v, DWORD_LittleEndian):
		return (v, winreg.REG_DWORD_LITTLE_ENDIAN)
	elif isinstance(v, DWORD):
		return (v, winreg.REG_DWORD)
	elif isinstance(v, Binary):
		return (v, winreg.REG_BINARY)
	# These are conversions from native types
	elif isinstance(v, basestring):
		return (String(v), winreg.REG_SZ)
	elif ( isinstance(v, list) or isinstance(v, tuple) or isinstance(v, set) or
               isinstance(v, enumerate) or isinstance(v, frozenset) or
               isinstance(v, GeneratorType) ):
		return (MultiString(v), winreg.REG_MULTI_SZ)
	elif isinstance(v, buffer):
		return (Binary(v), winreg.REG_BINARY)
	else:
		# Assume REG_NONE
		return (rNone(v), winreg.REG_NONE)

class _RegValues(DictMixin):
	__slots__=['parent']
	def __init__(self,parent):
		self.parent=parent
	def __len__(self):
		info = winreg.QueryInfoKey(self.parent.handle)
		return info[1]
	def __getitem__(self,key):
		val = winreg.QueryValueEx(self.parent.handle, key)
		return _Registry2Object(val[1],val[0]);
	def __setitem__(self,key,value):
		t = _Object2Registry(value)
		winreg.SetValueEx(self.parent.handle, key, 0, t[1], t[0])
	def __delitem__(self, key):
		winreg.DeleteValue(self.parent.handle, key)
	def keys(self):
		return list(self.__iter__())
	def __iter__(self):
		n = 0
		endoflist = False
		key = ""
		while not endoflist:
			try:
				key = winreg.EnumValue(self.parent.handle, n)
				n += 1
			except EnvironmentError:
				endoflist = True
				raise StopIteration
			else:
				if not endoflist:
					yield key[0]
	def iteritems(self):
		n = 0
		endoflist = False
		key = ""
		while not endoflist:
			try:
				key = winreg.EnumValue(self.parent.handle, n)
				n += 1
			except EnvironmentError:
				endoflist = True
				raise StopIteration
			else:
				if not endoflist:
					yield key[1]
	def __contains__(self, item):
		try:
			winreg.QueryValueEx(self.parent.handle, item)
		except WindowsError:
			return False
		else:
			return true

class _RegKeys(DictMixin):
	__slots__=['parent']
	def __init__(self,parent):
		self.parent=parent
	def __len__(self):
		info = winreg.QueryInfoKey(self.parent.handle)
		return info[0]
	def __getitem__(self,key):
		return Key(self.parent,key)
	def __delitem__(self, key):
		winreg.DeleteKey(self.parent.handle, key)
	def keys(self):
		return list(self.__iter__())
	def __iter__(self):
		n = 0
		endoflist = False
		while not endoflist:
			try:
				key = winreg.EnumKey(self.parent.handle, n)
				n += 1
			except EnvironmentError:
				endoflist = True
				raise StopIteration
			else:
				yield key
	def __contains__(self, item):
		try:
			hkey = winreg.OpenKey(self.parent.handle, key, 0, sam)
		except WindowsError:
			return False
		else:
			return true

class Key(object):
	"""The basic registry class."""
	__slots__=('handle','parent','myname','values','keys')
	def __init__(self, curkey=None, subkey='', hkey=None):
		"""Initializer. Don't pass anything to hkey, it is used internally."""
		subkey = unicode(subkey)
		if hkey is not None:
			self.handle=hkey
		else:
			self.handle = winreg.CreateKey(curkey.handle, subkey)
		self.parent=curkey
		self.myname=subkey
		self.values = _RegValues(self)
		self.keys = _RegKeys(self)
		
	def __del__(self):
		try: del self.values
		except: pass
		try: del self.keys
		except: pass
		try:
			winreg.CloseKey(self.handle)
			print "Key closed"
		except: pass
	def __repr__(self):
		return "<Registry Key: %s>" % self.getPath(False)
	def __str__(self):
		"""Returns the path of this key."""
		return self.getPath(True)
	def __div__(self, other):
		"""Not actually division, gets the subkey other (string).
		Equivelent to self.keys[other]"""
		return self.keys[other]
	def __truediv__(self, other):
		"""See Key.__div__"""
		return self.keys[other]
	def __getitem__(self, key):
		"""Returns the value of value key.
		Equivelent to self.values[key]."""
		return self.values[key]
	def __setitem__(self, key, value):
		"""Sets the value of value key.
		Equivelent to self.values[key] = value."""
		self.values[key] = value
	def __delitem__(self, key):
		"""Deletes the value key.
		Equivelent to del self.values[key]."""
		del self.values[key]
	def __contains__(self, item):
		"""Checks to see if item is a subkey of self.
		Item can be a key or string."""
		if isinstance(item, Key):
			return (self is item.parent)
		else:
			return item in self.key
	def getPath(self, abbrev=True):
		"""Returns the path of this key."""
		return "%s\\%s" % (self.parent.getPath(abbrev), self.myname)
	def flush(self):
		"""Ensures that this key is written to disk."""
		winreg.FlushKey(self.handle)
	def loadKey(self, key, file):
		"""Creates a subkey, loading information from the given file."""
		hkey = winreg.RegLoadKey(self.handle, key, file)
		return Key(self, key, hkey)
	def openKey(self, key, sam=winreg.KEY_READ):
		"""Opens a subkey, and returns a new Key object.
		Unlike instantiation, this fails if the key does not exist."""
		hkey = winreg.OpenKey(self.handle, key, 0, sam)
		return Key(self, key, hkey)
	def getMTime(self):
		"""Returns a datetime containing the time this key was last modified."""
		info = winreg.QueryInfoKey(self.handle)
		nsec = info[2]
		delta = timedelta(microseconds=nsec/10.0)
		epoch = datetime(1600, 1, 1)
		return epoch + delta
	def saveKey(self, filename):
		"""Saves this key to the file filename."""
		winreg.saveKey(self.handle, filename)

class _HKeyClassesRoot(Key):
	"""A subclass of Key to encapsulate HKEY_CLASSES_ROOT."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKCR"
		else:
			return "HKEY_CLASSES_ROOT"
HKEY_CLASSES_ROOT = _HKeyClassesRoot(hkey=winreg.HKEY_CLASSES_ROOT)

class _HKeyCurrentConfig(Key):
	"""A subclass of Key to encapsulate HKEY_CURRENT_CONFIG."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKCC"
		else:
			return "HKEY_CURRENT_CONFIG"
HKEY_CURRENT_CONFIG = _HKeyCurrentConfig(hkey=winreg.HKEY_CURRENT_CONFIG)

class _HKeyCurrentUser(Key):
	"""A subclass of Key to encapsulate HKEY_CURRENT_USER."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKCU"
		else:
			return "HKEY_CURRENT_USER"
HKEY_CURRENT_USER = _HKeyCurrentUser(hkey=winreg.HKEY_CURRENT_USER)

class _HKeyDynData(Key):
	"""A subclass of Key to encapsulate HKEY_DYN_DATA."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKDD"
		else:
			return "HKEY_DYN_DATA"
HKEY_DYN_DATA = _HKeyDynData(hkey=winreg.HKEY_DYN_DATA)

class _HKeyLocalMachine(Key):
	"""A subclass of Key to encapsulate HKEY_LOCAL_MACHINE."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKLM"
		else:
			return "HKEY_LOCAL_MACHINE"
HKEY_LOCAL_MACHINE = _HKeyLocalMachine(hkey=winreg.HKEY_LOCAL_MACHINE)

class _HKeyPerformanceData(Key):
	"""A subclass of Key to encapsulate HKEY_PERFORMANCE_DATA."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKPD"
		else:
			return "HKEY_PERFORMANCE_DATA"
HKEY_PERFORMANCE_DATA = _HKeyPerformanceData(hkey=winreg.HKEY_PERFORMANCE_DATA)

# HKEY_PERFORMANCE_NLSTEXT and HKEY_PERFORMANCE_TEXT would go
# here (New to XP), but they aren't available from _winreg.

class _HKeyUsers(Key):
	"""A subclass of Key to encapsulate HKEY_USERS."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKU"
		else:
			return "HKEY_USERS"
HKEY_USERS = _HKeyUsers(hkey=winreg.HKEY_USERS)

#Constants forwarded from _winreg
KEY_ALL_ACCESS          = winreg.KEY_ALL_ACCESS
KEY_CREATE_LINK         = winreg.KEY_CREATE_LINK
KEY_CREATE_SUB_KEY      = winreg.KEY_CREATE_SUB_KEY
KEY_ENUMERATE_SUB_KEYS  = winreg.KEY_ENUMERATE_SUB_KEYS
KEY_EXECUTE             = winreg.KEY_EXECUTE
KEY_NOTIFY              = winreg.KEY_NOTIFY
KEY_QUERY_VALUE         = winreg.KEY_QUERY_VALUE
KEY_READ                = winreg.KEY_READ
KEY_SET_VALUE           = winreg.KEY_SET_VALUE
KEY_WRITE               = winreg.KEY_WRITE
##REG_CREATED_NEW_KEY         = 1
##REG_FULL_RESOURCE_DESCRIPTOR = 9
##REG_LEGAL_CHANGE_FILTER = 15
##REG_LEGAL_OPTION = 15
##REG_NOTIFY_CHANGE_ATTRIBUTES = 2
##REG_NOTIFY_CHANGE_LAST_SET = 4
##REG_NOTIFY_CHANGE_NAME = 1
##REG_NOTIFY_CHANGE_SECURITY = 8
##REG_NO_LAZY_FLUSH = 4
##REG_OPENED_EXISTING_KEY = 2
##REG_OPTION_BACKUP_RESTORE = 4
##REG_OPTION_CREATE_LINK = 2
##REG_OPTION_NON_VOLATILE = 0
##REG_OPTION_OPEN_LINK = 8
##REG_OPTION_RESERVED = 0
##REG_OPTION_VOLATILE = 1
##REG_REFRESH_HIVE = 2
##REG_WHOLE_HIVE_VOLATILE = 1
