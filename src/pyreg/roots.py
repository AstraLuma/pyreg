"""
pyreg.roots - Defines the registry's roots (predefined keys)
By Jamie Bliss
Last modified $Date$
"""
from __future__ import absolute_import
import _winreg
from .key import Key

# _winreg doesn't define two roots:
#define HKEY_PERFORMANCE_TEXT       (( HKEY ) (ULONG_PTR)((LONG)0x80000050) )
_winreg.HKEY_PERFORMANCE_TEXT = -2147483568
#define HKEY_PERFORMANCE_NLSTEXT    (( HKEY ) (ULONG_PTR)((LONG)0x80000060) )
_winreg.HKEY_PERFORMANCE_NLSTEXT = -2147483552

__all__ = ('HKEY_CLASSES_ROOT', 'HKEY_CURRENT_CONFIG', 'HKEY_CURRENT_USER', 
	'HKEY_DYN_DATA', 'HKEY_LOCAL_MACHINE', 'HKEY_PERFORMANCE_DATA', 
	'HKEY_USERS')

class _HKeyRoot(Key):
	"""A subclass of Key to encapsulate HKEY_*."""
	def __repr__(self):
		return self.getPath(False)

class _HKeyClassesRoot(_HKeyRoot):
	"""A subclass of Key to encapsulate HKEY_CLASSES_ROOT."""
	def getPath(self, abbrev=True):
		if abbrev:
			return "HKCR"
		else:
			return "HKEY_CLASSES_ROOT"
HKEY_CLASSES_ROOT = _HKeyClassesRoot(hkey=_winreg.HKEY_CLASSES_ROOT)

class _HKeyCurrentConfig(_HKeyRoot):
	"""A subclass of Key to encapsulate HKEY_CURRENT_CONFIG."""
	def getPath(self, abbrev=True):
		if abbrev:
			return "HKCC"
		else:
			return "HKEY_CURRENT_CONFIG"
HKEY_CURRENT_CONFIG = _HKeyCurrentConfig(hkey=_winreg.HKEY_CURRENT_CONFIG)

class _HKeyCurrentUser(_HKeyRoot):
	"""A subclass of Key to encapsulate HKEY_CURRENT_USER."""
	def getPath(self, abbrev=True):
		if abbrev:
			return "HKCU"
		else:
			return "HKEY_CURRENT_USER"
HKEY_CURRENT_USER = _HKeyCurrentUser(hkey=_winreg.HKEY_CURRENT_USER)

class _HKeyDynData(_HKeyRoot):
	"""A subclass of Key to encapsulate HKEY_DYN_DATA."""
	def getPath(self, abbrev=True):
		if (abbrev):
			return "HKDD"
		else:
			return "HKEY_DYN_DATA"
HKEY_DYN_DATA = _HKeyDynData(hkey=_winreg.HKEY_DYN_DATA)

class _HKeyLocalMachine(_HKeyRoot):
	"""A subclass of Key to encapsulate HKEY_LOCAL_MACHINE."""
	def getPath(self, abbrev=True):
		if abbrev:
			return "HKLM"
		else:
			return "HKEY_LOCAL_MACHINE"
HKEY_LOCAL_MACHINE = _HKeyLocalMachine(hkey=_winreg.HKEY_LOCAL_MACHINE)

class _HKeyPerformanceData(_HKeyRoot):
	"""A subclass of Key to encapsulate HKEY_PERFORMANCE_DATA."""
	def getPath(self, abbrev=True):
		if abbrev:
			return "HKPD"
		else:
			return "HKEY_PERFORMANCE_DATA"
HKEY_PERFORMANCE_DATA = _HKeyPerformanceData(hkey=_winreg.HKEY_PERFORMANCE_DATA)

# HKEY_PERFORMANCE_NLSTEXT and HKEY_PERFORMANCE_TEXT would go
# here (New to XP), but they aren't available from _winreg.
# Screw it.

class _HKeyPerformanceNLSText(_HKeyRoot):
	"""A subclass of Key to encapsulate HKEY_PERFORMANCE_NLSTEXT."""
	def getPath(self, abbrev=True):
		if abbrev:
			return "HKPN"
		else:
			return "HKEY_PERFORMANCE_NLSTEXT"
HKEY_PERFORMANCE_NLSTEXT = _HKeyPerformanceNLSText(hkey=_winreg.HKEY_PERFORMANCE_NLSTEXT)

class _HKeyPerformanceText(_HKeyRoot):
	"""A subclass of Key to encapsulate HKEY_PERFORMANCE_TEXT."""
	def getPath(self, abbrev=True):
		if abbrev:
			return "HKPT"
		else:
			return "HKEY_PERFORMANCE_TEXT"
HKEY_PERFORMANCE_TEXT = _HKeyPerformanceNLSText(hkey=_winreg.HKEY_PERFORMANCE_TEXT)

class _HKeyUsers(_HKeyRoot):
	"""A subclass of Key to encapsulate HKEY_USERS."""
	def getPath(self, abbrev=True):
		if abbrev:
			return "HKU"
		else:
			return "HKEY_USERS"
HKEY_USERS = _HKeyUsers(hkey=_winreg.HKEY_USERS)
