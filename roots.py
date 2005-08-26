"""
pyreg.roots - Defines the registry's roots (predefined keys)
By Jamie Bliss
Last modified Augest 26, 2005
"""
import _winreg
from pyreg.key import *
##__all__ = ('HKEY_CLASSES_ROOT','HKEY_CURRENT_CONFIG','HKEY_CURRENT_USER','HKEY_DYN_DATA','HKEY_LOCAL_MACHINE','HKEY_PERFORMANCE_DATA','HKEY_USERS')

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
