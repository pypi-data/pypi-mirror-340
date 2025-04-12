'''
The python Plus - Pyplus
================
the python's plus library.\n
'''

from . import science ,tools
from site import getsitepackages
from toml import load

__all__=[
    "science" ,"tools",
    "VERSION","UPDATE_DOC", "UPDATE_TIME", "PRE_VERSION", "PRE_UPDATE_DOC", "PRE_UPDATE_TIME",
    "ALL", "NEW", "WILL", 
    "get_update", "get_version_update_time", "get_version", "get_pre_version", "get_news_update_time", "get_new", "get_all", "get_will", "get_pre_update", "get_pre_version_update_time", "get_pre_news_update_time", "get_pre_new", "get_pre_all"
]

VERSION = ""
UPDATE_DOC = {}
UPDATE_TIME = {}

PRE_VERSION = ""
PRE_UPDATE_DOC = {}
PRE_UPDATE_TIME = {}

ALL = "all"
NEW = "news"
WILL = "will"

def get_update(version: str): 
    '''get the version update doc.'''
    if version == ALL: 
        out_obj = UPDATE_DOC
    elif version == NEW: 
        out_obj = UPDATE_DOC.get(str(version), "This version is not found. Maybe it is not recorded.")
    elif version == WILL: 
        out_obj = UPDATE_DOC.get(WILL, "This version is not found. Maybe it is not recorded.")
    else: 
        out_obj = UPDATE_DOC.get(str(version), "This version is not found. Maybe it is not recorded.")
    print(out_obj)
    return out_obj

def get_version_update_time(version: str): 
    '''Get the version update time.'''
    if version == NEW: 
        out_obj = UPDATE_TIME.get(str(VERSION), "This version is not found. Maybe it is not recorded.")
    else: 
        out_obj = UPDATE_TIME.get(str(version), "This version is not found. Maybe it is not recorded.")
    print(out_obj)
    return out_obj

def get_will(): 
    '''Get the will update doc.'''
    return get_update(WILL)

def get_version():
    '''Get the version.'''
    return VERSION

def get_pre_version():
    '''Get the pre version.'''
    return PRE_VERSION

def get_news_update_time(): 
    '''Get the new update time.'''
    return get_version_update_time(NEW)

def get_new(): 
    '''Get the new update doc.'''
    return get_update(NEW)

def get_all(): 
    '''Get the all update doc.'''
    return get_update(ALL)

def get_will(): 
    '''Get the will update doc.'''
    return get_update(WILL)

def get_pre_update(version: str): 
    '''Get the pre-release version update doc.'''
    if version == ALL: 
        out_obj = PRE_UPDATE_DOC
    elif version == NEW: 
        out_obj = PRE_UPDATE_DOC.get(str(version))
    elif version == WILL: 
        out_obj = PRE_UPDATE_DOC.get(WILL, "This version is not found. Maybe it is not recorded.")
    else: 
        out_obj = PRE_UPDATE_DOC.get(str(version), "This version is not found. Maybe it is not recorded.")
    print(out_obj)
    return out_obj

def get_pre_version_update_time(version: str): 
    '''Get the pre-release version update time.'''
    if version == NEW: 
        out_obj = PRE_UPDATE_TIME.get(str(VERSION))
    else: 
        out_obj = PRE_UPDATE_TIME.get(str(version), "This version is not found. Maybe it is not recorded.")
    print(out_obj)
    return out_obj

def get_pre_news_update_time(): 
    '''Get the new update time.'''
    return get_pre_version_update_time(NEW)

def get_pre_new(): 
    '''Get the new pre-release update doc.'''
    return get_pre_update(NEW)

def get_pre_all(): 
    '''Get the all pre-release update doc.'''
    return get_pre_update(ALL)
