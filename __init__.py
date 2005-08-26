"""Defines classes to interface with the registry."""
import _winreg
import datetime
import sys
import types
import UserDict

##class pyregException(Exception):
##	"""An error occuried in the pyreg module."""
##class pyregWarning(RuntimeWarning, UserWarning):
##	"""A warning occuried in the pyreg module."""
##	
##class HKEYWrongOSVersion(pyregException):
##	"""The requested predefined key is not available in this version of Windows."""
##	key = 0

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
	def __init__(self,seq=None):
		if seq is not None:
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
	"""_Registry2Object(t,v) -> object
	
	Converts the given object and registry type to a registry type object."""
	if t == _winreg.REG_BINARY:
		return Binary(v)
	elif t == _winreg.REG_DWORD:
		return DWORD(v)
	elif t == _winreg.REG_DWORD_LITTLE_ENDIAN:
		return DWORD_LittleEndian(v)
	elif t == _winreg.REG_DWORD_BIG_ENDIAN:
		return DWORD_BigEndian(v)
	elif t == _winreg.REG_EXPAND_SZ:
		return ExpandingString(v)
	elif t == _winreg.REG_LINK:
		return Link(v)
	elif t == _winreg.REG_MULTI_SZ:
		return MultiString(v)
	elif t == _winreg.REG_NONE:
		return rNone(v)
	elif t == _winreg.REG_RESOURCE_LIST:
		return ResourceList(v)
	elif t == _winreg.REG_SZ:
		return String(v)
	else:
		# Assume REG_NONE
		return rNone(v)

def _Object2Registry(v):
	"""_Object2Registry(v) -> (object, int)
	
	Converts the given registry type object to a tuple containing a _winreg-compatible object and a type.
	You can also pass some native types, as follows:
	+ basestring -> REG_SZ
	+ list, tuple, set, enumerate, frozenset, generator -> REG_MULTI_SZ
	+ buffer -> REG_BINARY"""
	#We avoid inheritance problems by checking them in the reverse order they were defined
	if isinstance(v, String):
		return (v, _winreg.REG_SZ)
	elif isinstance(v, ResourceList):
		return (v, _winreg.REG_RESOURCE_LIST)
	elif isinstance(v, rNone):
		return (v, _winreg.REG_NONE)
	elif isinstance(v, MultiString):
		return (v, _winreg.REG_MULTI_SZ)
	elif isinstance(v, Link):
		return (v, _winreg.REG_LINK)
	elif isinstance(v, ExpandingString):
		return (v,_winreg.REG_EXPAND_SZ)
	elif isinstance(v, DWORD_BigEndian):
		return (v, _winreg.REG_DWORD_BIG_ENDIAN)
	elif isinstance(v, DWORD_LittleEndian):
		return (v, _winreg.REG_DWORD_LITTLE_ENDIAN)
	elif isinstance(v, DWORD):
		return (v, _winreg.REG_DWORD)
	elif isinstance(v, Binary):
		return (v, _winreg.REG_BINARY)
	# These are conversions from native types
	elif isinstance(v, basestring):
		return (String(v), _winreg.REG_SZ)
	elif ( isinstance(v, list) or isinstance(v, tuple) or isinstance(v, set) or
		isinstance(v, enumerate) or isinstance(v, frozenset) or
		isinstance(v, types.GeneratorType) ):
		return (MultiString(v), _winreg.REG_MULTI_SZ)
	elif isinstance(v, buffer):
		return (Binary(v), _winreg.REG_BINARY)
	else:
		# Assume REG_NONE
		return (rNone(v), _winreg.REG_NONE)

class _RegValues(UserDict.DictMixin):
	"""A dictionary wrapping the values of the key that created it. Don't
	instantiate yourself, use akey.values. Note that while it is a full
	dictionary, many of the methods don't make sense (eg, push() and pop())."""
	__slots__=('parent')
	def __init__(self,parent):
		self.parent=parent
	def __len__(self):
		"""x.__len__() <==> len(x)
		
		Returns the number of values in this key."""
		info = _winreg.QueryInfoKey(self.parent.handle)
		return info[1]
	def __getitem__(self,key):
		"""x.__getitem__(y) <==> x[y]
		
		Returns the contents of the given value, or creates a new one."""
		try:
			val = _winreg.QueryValueEx(self.parent.handle, key)
		except WindowsError:
			raise KeyError
		return _Registry2Object(val[1],val[0]);
	def __setitem__(self,key,value):
		"""x.__setitem__(i, y) <==> x[i]=y
		
		Sets the contents of the given value."""
		t = _Object2Registry(value)
		_winreg.SetValueEx(self.parent.handle, key, 0, t[1], t[0])
	def __delitem__(self, key):
		"""x.__delitem__(y) <==> del x[y]
		
		Deletes the given value."""
		_winreg.DeleteValue(self.parent.handle, key)
	def keys(self):
		"""k.keys() -> list
		
		Returns a list of subkeys.
		use iter() instead, this just calls that."""
		return list(self.__iter__())
	def __iter__(self):
		"""x.__iter__() <==> iter(x)
		
		Returns a generator that enumerates the names of the values."""
		n = 0
		endoflist = False
		key = ""
		while not endoflist:
			try:
				key = _winreg.EnumValue(self.parent.handle, n)
				n += 1
			except EnvironmentError:
				endoflist = True
				raise StopIteration
			else:
				if not endoflist:
					yield key[0]
	def iteritems(self):
		"""x.iteritems() -> generator
		
		Returns a generator that enumerates the names & contents of the values."""
		n = 0
		endoflist = False
		key = ""
		while not endoflist:
			try:
				key = _winreg.EnumValue(self.parent.handle, n)
				n += 1
			except EnvironmentError:
				endoflist = True
				raise StopIteration
			else:
				if not endoflist:
					yield (key[0], _Registry2Object(val[2],val[1]))
	def __contains__(self, item):
		"""v.__contains__(s) <==> s in v
		
		True if the given value exists."""
		try:
			_winreg.QueryValueEx(self.parent.handle, item)
		except WindowsError:
			return False
		else:
			return true

class _RegKeys(UserDict.DictMixin):
	"""A dictionary wrapping the subkeys of the key that created it. Don't
	instantiate yourself, use akey.keys. Note that while it is a full
	dictionary, many of the methods don't make sense (eg, push() and pop())."""
	__slots__=('parent')
	def __init__(self,parent):
		self.parent=parent
	def __len__(self):
		"""x.__len__() <==> len(x)
		
		Returns the number of subkeys in this key."""
		info = _winreg.QueryInfoKey(self.parent.handle)
		return info[0]
	def __getitem__(self,key):
		"""x.__getitem__(y) <==> x[y]
		
		Returns the Key of the given subkey, or creates a new one."""
		return Key(self.parent,key)
	def __delitem__(self, key):
		"""x.__delitem__(y) <==> del x[y]
		
		Deletes the given subkey."""
		_winreg.DeleteKey(self.parent.handle, key)
	def keys(self):
		"""k.keys() -> list
		
		Returns a list of subkeys.
		use iter() instead, this just calls that."""
		return list(self.__iter__())
	def __iter__(self):
		"""x.__iter__() <==> iter(x)
		
		Returns a generator that enumerates the names of the subkeys."""
		n = 0
		endoflist = False
		while not endoflist:
			try:
				key = _winreg.EnumKey(self.parent.handle, n)
				n += 1
			except EnvironmentError:
				endoflist = True
				raise StopIteration
			else:
				yield key
	def __contains__(self, item):
		"""k.__contains__(s) <==> s in k
		
		True if the given subkey exists."""
		try:
			hkey = _winreg.OpenKey(self.parent.handle, key, 0, sam)
		except WindowsError:
			return False
		else:
			return true

class Key(object):
	"""Wraps a registry key in a convenient way."""
	__slots__=('handle','parent','myname','values','keys')
	def __init__(self, curkey=None, subkey='', hkey=None):
		"""Initializer. Don't pass anything to hkey, it is used internally."""
		subkey = unicode(subkey)
		if hkey is not None:
			self.handle=hkey
		else:
			self.handle = _winreg.CreateKey(curkey.handle, subkey)
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
			_winreg.CloseKey(self.handle)
			print "Key closed"
		except: pass
	def __repr__(self):
		"""x.__repr__() <==> repr(x)"""
		return "<Registry Key: %s>" % self.getPath(False)
	def __str__(self):
		"""x.__str__() <==> str(x)
		
		Returns the path of this key."""
		return self.getPath(True)
	def __div__(self, other):
		"""x.__div__(y) <==> x/y
		
		Not actually division,. Gets the subkey other (string or Key).
		Equivelent to self.keys[other]"""
		return self.keys[other]
	def __truediv__(self, other):
		"""x.__truediv__(y) <==> x/y
		
		See Key.__div__()"""
		return self.keys[other]
	def __getitem__(self, key):
		"""x.__getitem__(y) <==> x[y]
		
		Returns the value of value key.
		Equivelent to self.values[key]."""
		return self.values[key]
	def __setitem__(self, key, value):
		"""x.__setitem__(i, y) <==> x[i]=y
		
		Sets the value of value key.
		Equivelent to self.values[key] = value."""
		self.values[key] = value
	def __delitem__(self, key):
		"""x.__delitem__(y) <==> del x[y]
		
		Deletes the value key. Equivelent to del self.values[key]."""
		del self.values[key]
	def __contains__(self, item):
		"""x.__contains__(y) <==> y in x
		
		Checks to see if item is a subkey of self.
		Item can be a key or string."""
		if isinstance(item, Key):
			return (self is item.parent)
		else:
			return item in self.key
	def getPath(self, abbrev=True):
		"""k.getPath([abbrev]) -> unicode
		
		Returns the path (eg, "HKCU\Software\Python 2.4") of the key
		wrapped by this key. If abbrev is False, the full root (eg, HKEY_CURRENT_USER)
		is used."""
		return unicode(u"%s\\%s" % (self.parent.getPath(abbrev), self.myname))
	def flush(self):
		"""k.flush() -> None
		
		Ensures that this key is written to disk. Calls _winreg.FlushKey(). See
		<http://msdn.microsoft.com/library/en-us/sysinfo/base/regflushkey.asp>"""
		_winreg.FlushKey(self.handle)
	def loadKey(self, key, file):
		"""k.loadKey(key, file) -> Key
		
		Opposite of saveKey().
		Creates and returns a subkey, loading information from the given file.
		Loads subkey key from file file. Only valid on HKEY_LOCAL_MACHINE and
		HKEY_USERS."""
		hkey = _winreg.RegLoadKey(self.handle, key, file)
		return Key(self, key, hkey)
	def saveKey(self, filename):
		"""k.saveKey(filename) -> None
		
		Opposite of loadKey(). Saves the currrent key to file filename."""
		_winreg.saveKey(self.handle, filename)
	def openKey(self, key, sam=_winreg.KEY_READ):
		"""k.openKey(key[, sam]) -> Key
		
		Identical to akey.keys[key], except an error is generated if the
		key does not exist. Also allows you to specify permissions in sam.
		Use the KEY_* constants for sam. See
		<http://msdn.microsoft.com/library/en-us/sysinfo/base/registry_key_security_and_access_rights.asp>
		for details."""
		hkey = _winreg.OpenKey(self.handle, key, 0, sam)
		return Key(self, key, hkey)
	def getmtime(self):
		"""k.getMTime() -> datetime.datetime
		
		Returns a datetime.datetime containing the time this key was last modified."""
		info = _winreg.QueryInfoKey(self.handle)
		nsec = info[2]
		delta = datetime.timedelta(microseconds=nsec/10.0)
		epoch = datetime.datetime(1600, 1, 1)
		return epoch + delta

class _HKeyClassesRoot(Key):
	"""A subclass of Key to encapsulate HKEY_CLASSES_ROOT."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKCR"
		else:
			return "HKEY_CLASSES_ROOT"
HKEY_CLASSES_ROOT = _HKeyClassesRoot(hkey=_winreg.HKEY_CLASSES_ROOT)

class _HKeyCurrentConfig(Key):
	"""A subclass of Key to encapsulate HKEY_CURRENT_CONFIG."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKCC"
		else:
			return "HKEY_CURRENT_CONFIG"
HKEY_CURRENT_CONFIG = _HKeyCurrentConfig(hkey=_winreg.HKEY_CURRENT_CONFIG)

class _HKeyCurrentUser(Key):
	"""A subclass of Key to encapsulate HKEY_CURRENT_USER."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKCU"
		else:
			return "HKEY_CURRENT_USER"
HKEY_CURRENT_USER = _HKeyCurrentUser(hkey=_winreg.HKEY_CURRENT_USER)

class _HKeyDynData(Key):
	"""A subclass of Key to encapsulate HKEY_DYN_DATA."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKDD"
		else:
			return "HKEY_DYN_DATA"
HKEY_DYN_DATA = _HKeyDynData(hkey=_winreg.HKEY_DYN_DATA)

class _HKeyLocalMachine(Key):
	"""A subclass of Key to encapsulate HKEY_LOCAL_MACHINE."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKLM"
		else:
			return "HKEY_LOCAL_MACHINE"
HKEY_LOCAL_MACHINE = _HKeyLocalMachine(hkey=_winreg.HKEY_LOCAL_MACHINE)

class _HKeyPerformanceData(Key):
	"""A subclass of Key to encapsulate HKEY_PERFORMANCE_DATA."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKPD"
		else:
			return "HKEY_PERFORMANCE_DATA"
HKEY_PERFORMANCE_DATA = _HKeyPerformanceData(hkey=_winreg.HKEY_PERFORMANCE_DATA)

# HKEY_PERFORMANCE_NLSTEXT and HKEY_PERFORMANCE_TEXT would go
# here (New to XP), but they aren't available from _winreg.

class _HKeyUsers(Key):
	"""A subclass of Key to encapsulate HKEY_USERS."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKU"
		else:
			return "HKEY_USERS"
HKEY_USERS = _HKeyUsers(hkey=_winreg.HKEY_USERS)

#Constants forwarded from _winreg
KEY_ALL_ACCESS          = _winreg.KEY_ALL_ACCESS
KEY_CREATE_LINK         = _winreg.KEY_CREATE_LINK
KEY_CREATE_SUB_KEY      = _winreg.KEY_CREATE_SUB_KEY
KEY_ENUMERATE_SUB_KEYS  = _winreg.KEY_ENUMERATE_SUB_KEYS
KEY_EXECUTE             = _winreg.KEY_EXECUTE
KEY_NOTIFY              = _winreg.KEY_NOTIFY
KEY_QUERY_VALUE         = _winreg.KEY_QUERY_VALUE
KEY_READ                = _winreg.KEY_READ
KEY_SET_VALUE           = _winreg.KEY_SET_VALUE
KEY_WRITE               = _winreg.KEY_WRITE
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
