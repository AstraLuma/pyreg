"""
pyreg.types - Defines classes to wrap the registry's types
By Jamie Bliss
Last modified $Date$
"""
import _winreg

__all__=('Binary','DWORD','DWORD_BigEndian','DWORD_LittleEndian','ExpandingString','Link','MultiString','ResourceList','String','rNone')

_generator = (x for x in [0]).__class__


class Binary(str):
	"""MSDN: "Binary data in any form."
	
	Encapsulates the REG_BINARY type; based on str."""
	#TODO: Override __str__ so it prints hex.
	pass

class DWORD(long):
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
	def __toregistry__(self):
		# We have to convert to a signed 4-byte interger. _winreg is lame that way.
		if (self >= 0x80000000):
			return int(self - 0x100000000)
		else:
			return self
	@staticmethod
	def __fromregistry__(v):
		return DWORD(v & 0xFFFFFFFF)

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
	@staticmethod
	def __fromregistry__(v):
		x = ord(v[3]) | ord(v[2])<<8 | ord(v[1])<<16 | ord(v[0])<<24
		return DWORD_BigEndian(x)
	def __toregistry__(self):
		rtn = ''
		rtn = chr( self        & 0xFF) + rtn
		rtn = chr((self >>  8) & 0xFF) + rtn
		rtn = chr((self >> 16) & 0xFF) + rtn
		rtn = chr((self >> 24) & 0xFF) + rtn
		return rtn

class ExpandingString(unicode):
	"""MDSN: "A null-terminated string that contains unexpanded references to environment variables (for example, "%PATH%"). It will be a Unicode or ANSI string depending on whether you use the Unicode or ANSI functions. To expand the environment variable references, use the ExpandEnvironmentStrings function."

	Encapsulates REG_EXPAND_SZ, based on unicode."""
	pass


class Link(unicode):
	"""MSDN: "A Unicode symbolic link. Used internally; applications should not use this type."
	
	Encapsulates REG_LINK, based on unicode."""
	@staticmethod
	def __fromregistry__(v):
		return Link(v, 'utf-16le', 'replace')
	def __toregistry__(self):
		return self

class MultiString(list):
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
		return DWORD.__fromregistry__(v)
	elif t == _winreg.REG_DWORD_LITTLE_ENDIAN:
		return DWORD_LittleEndian.__registry__(v)
	elif t == _winreg.REG_DWORD_BIG_ENDIAN:
		return DWORD_BigEndian.__fromregistry__(v)
	elif t == _winreg.REG_EXPAND_SZ:
		return ExpandingString(v)
	elif t == _winreg.REG_LINK:
		return Link.__fromregistry__(v)
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
		return (v.__toregistry__(), _winreg.REG_LINK)
	elif isinstance(v, ExpandingString):
		return (v,_winreg.REG_EXPAND_SZ)
	elif isinstance(v, DWORD_BigEndian):
		return (v.__toregistry__(), _winreg.REG_DWORD_BIG_ENDIAN)
	elif isinstance(v, DWORD_LittleEndian):
		return (v.__toregistry__(), _winreg.REG_DWORD_LITTLE_ENDIAN)
	elif isinstance(v, DWORD):
		return (v.__toregistry__(), _winreg.REG_DWORD)
	elif isinstance(v, Binary):
		return (v, _winreg.REG_BINARY)
	# These are conversions from native types
	elif isinstance(v, basestring):
		return (String(v), _winreg.REG_SZ)
	elif ( isinstance(v, list) or isinstance(v, tuple) or isinstance(v, set) or
		isinstance(v, enumerate) or isinstance(v, frozenset) or
		isinstance(v, _generator) ):
		return (MultiString(v), _winreg.REG_MULTI_SZ)
	elif isinstance(v, buffer):
		return (Binary(v), _winreg.REG_BINARY)
	elif isinstance(v, long) or isinstance(v, int):
		return (DWORD(v).__toregistry__(), _winreg.REG_BINARY)
	else:
		#print "Unknown type:",v.__class__,"-",repr(v)
		#If it has a __registry__ method, call that first.
		if hasattr(v, '__registry__') and callable(v.__registry__):
			o = v.__registry__()
			return _Object2Registry(o)
		else:
			# assume REG_NONE
			return (rNone(v), _winreg.REG_NONE)
