"""
pyreg.types - Defines classes to wrap the registry's types
By Jamie Bliss
Last modified Augest 26, 2005
"""
__all__=('Binary','DWORD','DWORD_BigEndian','DWORD_LittleEndian','ExpandingString','Link','MultiString','ResourceList','String','rNone')
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
