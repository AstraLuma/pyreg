"""
pyreg.types - Defines classes to wrap the registry's types
By Jamie Bliss
Last modified $Date$
"""
import _winreg
#import types ## Conflicts with this module
__all__ = ('Binary', 'DWORD', 'DWORD_BigEndian', 'DWORD_LittleEndian', 'ExpandingString', 'Link', 'MultiString', 'ResourceList', 'String', 'rNone')

_GeneratorType = (i for i in []).__class__

## Not a new-style object because we don't need the extras.
class RegistryType:
	"""Provides default implementation for registry methods."""
	@classmethod
	def __from_registry__(cls, val):
		"""Converts registry data to an instance of this class. Must be a classmethod or a staticmethod. Takes one argument, the value."""
		return cls(val)

	def __to_registry__(self):
		"""Converts this instance to something _winreg understands. Returns either an instance of a class in the  in the _registryDataClasses, or a two-tuple."""
		return self

class Binary(str, RegistryType):
	"""MSDN: "Binary data in any form."
	
	Encapsulates the REG_BINARY type; based on str."""
	#TODO: Override __str__ so it prints hex.

class DWORD(long, RegistryType):
	"""MSDN: "A 32-bit number."
	
	Encapsulates the REG_DWORD type.
	Exactly like long, except it is limited to 0-0xFFFFFFFF."""
	def __new__(cls, x, base=False):
		if base is False:
			inst = super(DWORD, cls).__new__(cls, x)
		else:
			inst = super(DWORD, cls).__new__(cls, x, base)
		if long(inst & 0xFFFFFFFF) != long(inst):
			inst = DWORD(inst & 0xFFFFFFFF)
		return inst
	
	def __to_registry__(self):
		# We have to convert to a signed 4-byte interger. _winreg is lame that way.
		if (self >= 0x80000000):
			return int(self - 0x100000000)
		else:
			return self
	
	@classmethod
	def __from_registry__(cls, v):
		return cls(v & 0xFFFFFFFF)

class DWORD_LittleEndian(DWORD):
	"""MSDN: "A 32-bit number in little-endian format. This is equivalent to REG_DWORD.
	In little-endian format, a multi-byte value is stored in memory from the lowest byte (the "little end") to the highest byte. For example, the value 0x12345678 is stored as (0x78 0x56 0x34 0x12) in little-endian format.
	Windows NT/Windows 2000, Windows 95, and Windows 98 are designed to run on little-endian computer architectures. A user may connect to computers that have big-endian architectures, such as some UNIX systems."
	
	Encapsulates REG_DWORD_LITTLE_ENDIAN; identical to DWORD"""
	pass

class DWORD_BigEndian(DWORD):
	"""MSDN: "A 32-bit number in big-endian format.
	In big-endian format, a multi-byte value is stored in memory from the highest byte (the "big end") to the lowest byte. For example, the value 0x12345678 is stored as (0x12 0x34 0x56 0x78) in big-endian format."

	Encapsulates REG_DWORD_BIG_ENDIAN, behaves like DWORD."""
	@classmethod
	def __from_registry__(cls, v):
		x = ord(v[3]) | ord(v[2])<<8 | ord(v[1])<<16 | ord(v[0])<<24
		return cls(x)
	
	def __to_registry__(self):
		rtn = ''
		rtn = chr( self        & 0xFF) + rtn
		rtn = chr((self >>  8) & 0xFF) + rtn
		rtn = chr((self >> 16) & 0xFF) + rtn
		rtn = chr((self >> 24) & 0xFF) + rtn
		return rtn

class ExpandingString(unicode, RegistryType):
	"""MDSN: "A null-terminated string that contains unexpanded references to environment variables (for example, "%PATH%"). It will be a Unicode or ANSI string depending on whether you use the Unicode or ANSI functions. To expand the environment variable references, use the ExpandEnvironmentStrings function."

	Encapsulates REG_EXPAND_SZ, based on unicode."""
	pass


class Link(unicode, RegistryType):
	"""MSDN: "A Unicode symbolic link. Used internally; applications should not use this type."
	
	Encapsulates REG_LINK, based on unicode."""
	
	@classmethod
	def __from_registry__(cls, v):
		return cls(v, 'utf-16le', 'replace')
	
	def __to_registry__(self):
		return self

class MultiString(list, RegistryType):
	"""MSDN: "An array of null-terminated strings, terminated by two null characters."

	Encapsulates REG_MULTI_SZ; based on list.
	Make sure you only pass strings (or stuff convertable to strings) to it, it will
	raise a TypeError otherwise."""
	def __init__(self,seq=None):
		"""x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
		if seq is not None:
			val = [unicode(i) for i in seq]
			list.__init__(self, val)
		else:
			list.__init__(self)
	def __setitem__(self, key, value):
		"""x.__setitem__(i, y) <==> x[i]=y"""
		if isinstance(key, slice):
			seq = [unicode(i) for i in value]
		else:
			seq = unicode(value)
		list.__setitem__(self, key, seq)
	def __setslice__(self, i, j, sequence):
		"""x.__setslice__(i, j, y) <==> x[i:j]=y

               Use  of negative indices is not supported."""
		val = [unicode(i) for i in sequence]
		list.__setslice__(self, i, j, sequence)
	def append(self,x):
		"""L.append(object) -- append object to end"""
		v = unicode(x)
		list.append(self,v)

class rNone(Binary):
	"""MSDN: "No defined value type."

	Wraps REG_NONE, identical to Binary."""
	pass

class ResourceList(Binary):
	"""MSDN: "A device-driver resource list."

	Encapsulates REG_RESOURCE_LIST; behaves like Binary."""
	pass

class String(unicode, RegistryType):
	"""MDSN: "A null-terminated string. It will be a Unicode or ANSI string, depending on whether you use the Unicode or ANSI functions."

	Encapsulates REG_SZ, based on unicode. (strings are always Unicode due to _winreg implementation.)"""
	pass

_registryDataClasses = {
	_winreg.REG_BINARY : Binary,
	_winreg.REG_DWORD : DWORD,
	_winreg.REG_DWORD_LITTLE_ENDIAN : DWORD_LittleEndian,
	_winreg.REG_DWORD_BIG_ENDIAN : DWORD_BigEndian,
	_winreg.REG_EXPAND_SZ : ExpandingString,
	_winreg.REG_LINK : Link,
	_winreg.REG_MULTI_SZ : MultiString,
	_winreg.REG_NONE : rNone,
	_winreg.REG_RESOURCE_LIST : ResourceList,
	_winreg.REG_SZ : String,
}
"""A dictionary linking the registry data type constants (keys) to the classes that handle them (values)."""

_dict_index = lambda d, v: d.keys()[d.values().index(v)] ## There's gotta be a better way to do that

def _Registry2Object(t,v):
	"""_Registry2Object(t,v) -> object
	
	Converts the given object and registry type to a registry type object."""
	if t in _registryDataClasses:
		return _registryDataClasses[t].__from_registry__(v)
	else:
		# Assume REG_NONE
		return rNone.__from_registry__(v)
def _Object2Registry(v):
	"""_Object2Registry(v) -> (object, int)
	
	Converts the given registry type object to a tuple containing a _winreg-compatible object and a type.
	You can also pass some native types, as follows:
	+ basestring -> String
	+ list, tuple, set, enumerate, frozenset, generator -> MultiString
	+ buffer -> Binary
	+ long, int -> DWORD
	+ None -> null rNone
	+ bool -> DWORD (-1 or 0)"""
	for __aNumberIDontUseButNeedToTrackThisLoopWith in range(0, 2):
		## A known type
		if v.__class__ in _registryDataClasses.values():
			t = _dict_index(_registryDataClasses, v.__class__)
			return (v.__to_registry__(), t)
		elif hasattr(v, '__to_registry__'):
			v = v.__to_registry__()
		## These are conversions from native types
		## Must be last so that inheritance trees don't screw it up
		elif isinstance(v, basestring):
			return _Object2Registry(String(v))
		elif ( isinstance(v, list) or isinstance(v, tuple) or isinstance(v, set) or
				isinstance(v, enumerate) or isinstance(v, frozenset) or
				isinstance(v, _GeneratorType) ):
			return _Object2Registry(MultiString(v))
		elif isinstance(v, buffer):
			return _Object2Registry(Binary(v))
		elif isinstance(v, long) or isinstance(v, int):
			return (DWORD(v).__to_registry__(), _winreg.REG_DWORD)
		## These types don't cleanly convert to another type
		elif isinstance(v, None.__class__):
			return ('', _winreg.REG_NONE)
		elif isinstance(v, bool):
			if v: return (0xFFFFFFFF, _winreg.REG_DWORD)
			else: return (0, _winreg.REG_DWORD)
	raise TypeError("The variable you passed can't be converted to a type acceptable by _winreg")
