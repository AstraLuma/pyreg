"""Defines classes to interface with the registry."""
import _winreg as winreg
import datetime
from datetime import timedelta, date, time, datetime
import sys

class pyregException(Exception):
    """An error occuried in the pyreg module."""
class pyregWarning(RuntimeWarning, UserWarning):
    """A warning occuried in the pyreg module."""
    
class HKEYWrongOSVersion(pyregException):
    """The requested predefined key is not available in this version of Windows."""
    key = 0

class Key:
    """The basic registry class
    TODO: Add operators (for subkeys or values?)"""
    handle = 0
    parent = 0
    myname = ""
    def __init__(self, curkey, subkey, hkey=False):
        """Initializer. Don't pass anything to hkey, it is used internally."""
        if (hkey):
            self.handle = hkey
        else:
            self.handle = winreg.CreateKey(curkey.handle, subkey)
        self.parent = curkey
        self.myname = subkey
        
    def __del__(self):
        winreg.CloseKey(self.handle)
    def __repr__(self):
        return "<Registry Key: %s>" % self.getPath(False)
    def __str__(self):
        return self.getPath(True)
    def getPath(abbrev=True):
        return "%s\\%s" % (self.parent.getPath(abbrev), self.myname)
    def deleteKey(self, subkey):
        """Deletes a subkey of the current key."""
        winreg.DeleteKey(self.handle, subkey)
    def deleteValue(self,name):
        """Deletes a value of the current key (Can't delete the None value!)"""
        winreg.DeleteValue(self.handle, name)
    def enumKeys(self):
        """Creates a generator to enumerate child keys."""
        n = 0
        endoflist = False
        while not endoflist:
            try:
                key = winreg.EnumKey(self.handle, n)
            except EnvironmentError:
                #We'll skip this, just the end of the list
                endoflist = True
            else:
                yield value
    def enumValues(self):
        """Creates a generator to enumerate values. (Including the implied None.)"""
        n = 0
        endoflist = False
        while not endoflist:
            try:
                key = winreg.EnumValue(self.handle, n)
            except EnvironmentError:
                #We'll skip this, just the end of the list
                endoflist = True
            else:
                yield value
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
    def countKeys(self):
        """Returns the number of subkeys."""
        info = winreg.QueryInfoKey(self.handle)
        return info[0]
    def countValues(self):
        """Returns the number of values (including the implied None)."""
        info = winreg.QueryInfoKey(self.handle)
        return info[1]
    def getMDate(self):
        info = winreg.QueryInfoKey(self.handle)
        nsec = info[2]
        delta = timedelta(microseconds=nsec/10.0)
        epoch = date(1600, 1, 1)
        return epoch + delta
    def getValue(self, valuename):
        """Returns the value of the value valuename."""
        val = winreg.QueryValueEx(self.handle, valuename)
        return val[0]
    def getValueType(self, valuename):
        """Returns the type of the value valuename."""
        val = winreg.QueryValueEx(self.handle, valuename)
        return val[1]
    def saveKey(self, filename):
        """Saves this key to the file filename."""
        winreg.saveKey(self.handle, filename)
    def setValue(self, valuename, valuecontents, valuetype=None):
        """Sets the value valuename to valuecontents and the type to valuetype (if provided)."""
        if (valuetype == None):
            valuetype = self.getValueType(valuename)
        winreg.SetValueEx(self.handle, valuename, 0, valuetype, valuecontents)

class HKeyClassesRoot(Key):
    """A subclass of Key to encapsulate HKEY_CLASSES_ROOT."""
    def __init__(self, curkey=None, subkey=None, hkey=winreg.HKEY_CLASSES_ROOT):
        """Initializer. All arguments are ignored."""
        self.handle = winreg.HKEY_CLASSES_ROOT
    def __del__(self):
        pass
    def getPath(abbrev=True):
        if (abbrev):
            return "HKCR"
        else:
            return "HKEY_CLASSES_ROOT"

class HKeyCurrentConfig(Key):
    """A subclass of Key to encapsulate HKEY_CURRENT_CONFIG."""
    def __init__(self, curkey=None, subkey=None, hkey=winreg.HKEY_CURRENT_CONFIG):
        """Initializer. All arguments are ignored."""
        ver = sys.getwindowsversion()
        if (not ( ver[3] == sys.VER_PLATFORM_WIN32_WINDOWS or
                  ( ver[3] == VER_PLATFORM_WIN32_NT and ver[0] >= 4 )
                )):
            ex = HKEYWrongOSVersion()
            ex.key = winreg.HKEY_CURRENT_CONFIG
            raise ex
        self.handle = winreg.HKEY_CURRENT_CONFIG
    def __del__(self):
        pass
    def getPath(abbrev=True):
        if (abbrev):
            return "HKCC"
        else:
            return "HKEY_CURRENT_CONFIG"

class HKeyCurrentUser(Key):
    """A subclass of Key to encapsulate HKEY_CURRENT_USER."""
    def __init__(self, curkey=None, subkey=None, hkey=winreg.HKEY_CURRENT_USER):
        """Initializer. All arguments are ignored."""
        self.handle = winreg.HKEY_CURRENT_USER
    def __del__(self):
        pass
    def getPath(abbrev=True):
        if (abbrev):
            return "HKCU"
        else:
            return "HKEY_CURRENT_USER"

class HKeyDynData(Key):
    """A subclass of Key to encapsulate HKEY_DYN_DATA."""
    def __init__(self, curkey=None, subkey=None, hkey=winreg.HKEY_DYN_DATA):
        """Initializer. All arguments are ignored."""
        ver = sys.getwindowsversion()
        if (not ( ver[3] == sys.VER_PLATFORM_WIN32_WINDOWS )):
            ex = HKEYWrongOSVersion()
            ex.key = winreg.HKEY_DYN_DATA
            raise ex
        self.handle = winreg.HKEY_DYN_DATA
    def __del__(self):
        pass
    def getPath(abbrev=True):
        if (abbrev):
            return "HKDD"
        else:
            return "HKEY_DYN_DATA"

class HKeyLocalMachine(Key):
    """A subclass of Key to encapsulate HKEY_LOCAL_MACHINE."""
    def __init__(self, curkey=None, subkey=None, hkey=winreg.HKEY_LOCAL_MACHINE):
        """Initializer. All arguments are ignored."""
        self.handle = winreg.HKEY_LOCAL_MACHINE
    def __del__(self):
        pass
    def getPath(abbrev=True):
        if (abbrev):
            return "HKLM"
        else:
            return "HKEY_LOCAL_MACHINE"

class HKeyPerformanceData(Key):
    """A subclass of Key to encapsulate HKEY_DYN_DATA."""
    def __init__(self, curkey=None, subkey=None, hkey=winreg.HKEY_PERFORMANCE_DATA):
        """Initializer. All arguments are ignored."""
        ver = sys.getwindowsversion()
        if (not ( ver[3] == sys.VER_PLATFORM_WIN32_NT )):
            ex = HKEYWrongOSVersion()
            ex.key = winreg.HKEY_PERFORMANCE_DATA
            raise ex
        self.handle = winreg.HKEY_PERFORMANCE_DATA
    def __del__(self):
        pass
    def getPath(abbrev=True):
        if (abbrev):
            return "HKPD"
        else:
            return "HKEY_PERFORMANCE_DATA"

# HKEY_PERFORMANCE_NLSTEXT and HKEY_PERFORMANCE_TEXT would go
# here (New to XP), but they aren't available from _winreg.

class HKeyUsers(Key):
    """A subclass of Key to encapsulate HKEY_LOCAL_MACHINE."""
    def __init__(self, curkey=None, subkey=None, hkey=winreg.HKEY_USERS):
        """Initializer. All arguments are ignored."""
        self.handle = winreg.HKEY_USERS
    def __del__(self):
        pass
    def getPath(abbrev=True):
        if (abbrev):
            return "HKU"
        else:
            return "HKEY_USERS"
