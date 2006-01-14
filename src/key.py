"""
pyreg.key - Defines the Key class
By Jamie Bliss
Last modified $Date$
"""
import _winreg
import datetime
import sys
import UserDict
from pyreg.types import Binary,DWORD,DWORD_BigEndian,DWORD_LittleEndian,ExpandingString,Link,MultiString,ResourceList,String,rNone,_Registry2Object,_Object2Registry

__all__=('Key', 'ValueReference')

# These functions are new (to me):
# * GetSystemRegistryQuota
# * RegDeleteKeyEx
# * RegDisableReflectionKey
# * RegEnableReflectionKey
# * RegGetValue
# * RegQueryReflectionKey

class ValueReference(object):
	"""A reference to a value, allows you to pass a reference to a registry value.
	
	There aren't any meta-data functions because they would be as expensive as just dereferencing."""
	parent = None
	value = None
	def __init__(self, parent, value):
		self.parent = parent
		self.value = value
	
	def __call__(self):
		"""Get the actual value that this references."""
		return self.parent.values[self.value]

class _RegValues(UserDict.DictMixin):
	"""A dictionary wrapping the values of the key that created it. Don't
	instantiate yourself, use akey.values. Note that while it is a full
	dictionary, many of the methods don't make sense (eg, push() and pop())."""
	__slots__=('parent')
	def __init__(self, parent):
		self.parent=parent
	def __len__(self):
		"""x.__len__() <==> len(x)
		
		Returns the number of values in this key."""
		info = _winreg.QueryInfoKey(self.parent._handle)
		return info[1]
	def ref(self, key):
		"""Returns a reference to the value; see ValueReference."""
		return ValueReference(self.parent, key)
	def __getitem__(self, key):
		"""x.__getitem__(y) <==> x[y]
		
		Returns the contents of the given value, or creates a new one."""
		try:
			val = _winreg.QueryValueEx(self.parent._handle, key)
		except WindowsError:
			raise KeyError
		return _Registry2Object(val[1],val[0]);
	def __setitem__(self, key, value):
		"""x.__setitem__(i, y) <==> x[i]=y
		
		Sets the contents of the given value."""
		t = _Object2Registry(value)
		try: _winreg.SetValueEx(self.parent._handle, key, 0, t[1], t[0])
		except:
                    print (self.parent.handle, key, 0, t[1], t[0])
                    raise
	def __delitem__(self, key):
		"""x.__delitem__(y) <==> del x[y]
		
		Deletes the given value."""
		_winreg.DeleteValue(self.parent._handle, key)
	def keys(self):
		"""k.keys() -> list
		
		Returns a list of subkeys.
		use iter() instead, this just calls that."""
		return list(self.__iter__())
	def __iter__(self):
		"""x.__iter__() <==> iter(x)
		
		Returns a generator that enumerates the names of the values."""
		n = 0
		key = ""
		while True:
			try:
				key = _winreg.EnumValue(self.parent._handle, n)
				n += 1
			except EnvironmentError:
				break
			else:
				yield key[0]
	def iteritems(self):
		"""x.iteritems() -> generator
		
		Returns a generator that enumerates the names & contents of the values."""
		n = 0
		key = ""
		while True:
			try:
				key = _winreg.EnumValue(self.parent._handle, n)
				n += 1
			except EnvironmentError:
				break
			else:
				yield (key[0], _Registry2Object(key[2],key[1]))
	def __contains__(self, item):
		"""v.__contains__(s) <==> s in v
		
		True if the given value exists."""
		try:
			_winreg.QueryValueEx(self.parent._handle, item)
		except WindowsError:
			return False
		else:
			return True
	
	def copy(self):
		"""D.copy() -> a shallow copy of D"""
		value = {}
		for i in self.iteritems(): value[i[0]] = i[1]
		return value
	def update(self, dict, **kwargs):
		"""D.update(E, **F) -> None.  Upadte D from E and F: for k in E: D[k] = E[k]
		(if E has keys else: for (k, v) in E: D[k] = v) then: for k in F: D[k] = F[k]"""
		try:
			for k in dict: self[k] = dict[k]
		except TypeError:
			try:
				for (k, v) in dict: self[k] = v
			except: pass
		for k in kwargs: self[k] = kwargs[k]

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
		info = _winreg.QueryInfoKey(self.parent._handle)
		return info[0]
	def __getitem__(self,key):
		"""x.__getitem__(y) <==> x[y]
		
		Returns the Key of the given subkey, or creates a new one."""
		return Key(self.parent,key)
	def __delitem__(self, key):
		"""x.__delitem__(y) <==> del x[y]
		
		Deletes the given subkey."""
		_winreg.DeleteKey(self.parent._handle, key)
	def keys(self):
		"""k.keys() -> list
		
		Returns a list of subkeys.
		Use iter() instead, this just calls that."""
		return list(self.__iter__())
	def __iter__(self):
		"""x.__iter__() <==> iter(x)
		
		Returns a generator that enumerates the names of the subkeys."""
		n = 0
		while True:
			try:
				key = _winreg.EnumKey(self.parent._handle, n)
				n += 1
			except EnvironmentError:
				break
			else:
				yield key
	def __contains__(self, item):
		"""k.__contains__(s) <==> s in k
		
		True if the given subkey exists."""
		try:
			hkey = _winreg.OpenKey(self.parent._handle, item)
		except WindowsError:
			return False
		else:
			return True

class Key(object):
	"""Wraps a registry key in a convenient way."""
	__slots__=('_handle','parent','myname','values','keys')
	def __init__(self, curkey=None, subkey='', hkey=None):
		"""Initializer. Don't pass anything to hkey, it is used internally."""
		subkey = unicode(subkey)
		if hkey is not None:
			self._handle=hkey
		else:
			self._handle = _winreg.CreateKey(curkey._handle, subkey)
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
			_winreg.CloseKey(self._handle)
		except: pass
	def __repr__(self):
		"""x.__repr__() <==> repr(x)"""
		return "%r/%r" % (self.parent, self.myname)
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
		
		Checks to see if item is a subkey of self. Item can be a key or 
		string. This is not recursive."""
		if isinstance(item, Key):
			return (self is item.parent)
		else:
			return item in self.keys
	def __or__(self, val):
		"""x.__or__(y) <==> x|y
		
		Returns the given value. Equivelent to x.values[y].
		Note that the selection of the operator was rather arbitrary. It
		could have been anything with a lower precedence than division."""
		return self.values[val]
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
		hkey = _winreg.RegLoadKey(self._handle, key, file)
		return Key(self, key, hkey)
	def saveKey(self, filename):
		"""k.saveKey(filename) -> None
		
		Opposite of loadKey(). Saves the currrent key to file filename."""
		_winreg.saveKey(self._handle, filename)
	def openKey(self, key, sam=_winreg.KEY_READ):
		"""k.openKey(key[, sam]) -> Key
		
		Identical to akey.keys[key], except an error is generated if the
		key does not exist. Also allows you to specify permissions in sam.
		Use the KEY_* constants for sam. See
		<http://msdn.microsoft.com/library/en-us/sysinfo/base/registry_key_security_and_access_rights.asp>
		for details."""
		hkey = _winreg.OpenKey(self._handle, key, 0, sam)
		return Key(self, key, hkey)
	def getmtime(self):
		"""k.getMTime() -> datetime.datetime
		
		Returns a datetime.datetime containing the time this key was last modified."""
		info = _winreg.QueryInfoKey(self._handle)
		nsec = info[2]
		delta = datetime.timedelta(microseconds=nsec/10.0)
		epoch = datetime.datetime(1600, 1, 1)
		return epoch + delta
