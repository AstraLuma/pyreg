"""
pyreg - Defines classes to interface with the registry.
By Jamie Bliss
Last modified Augest 26, 2005
"""
import _winreg
from pyreg.types import *
from pyreg.key import *
from pyreg.roots import *

##class pyregException(Exception):
##	"""An error occuried in the pyreg module."""
##class pyregWarning(RuntimeWarning, UserWarning):
##	"""A warning occuried in the pyreg module."""
##	
##class HKEYWrongOSVersion(pyregException):
##	"""The requested predefined key is not available in this version of Windows."""
##	key = 0

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
