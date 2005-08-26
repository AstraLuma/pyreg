"""
pyreg.key - Defines the Key class
By Jamie Bliss
Last modified Augest 26, 2005
"""
import _winreg
import datetime
import sys
import types
import UserDict
from pyreg.types import Binary,DWORD,DWORD_BigEndian,DWORD_LittleEndian,ExpandingString,Link,MultiString,ResourceList,String,rNone
__all__=('Key')

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
