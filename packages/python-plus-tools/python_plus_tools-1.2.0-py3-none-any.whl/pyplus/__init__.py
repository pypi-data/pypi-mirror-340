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

updates = load(open(getsitepackages()[1]+"\\pyplus\\update.toml", "r", encoding="utf-8"))

ALL = "all"
NEW = "news"
WILL = "will"

def get_update(namespace:str, version: str): 
    '''get the version update doc.'''
    try:
        open_dict = updates['release'][namespace]['update_info']
    except KeyError:
        raise ValueError('This namespace not found.')

    if version == ALL: 
        out_obj = open_dict
    elif version == NEW: 
        out_obj = open_dict.get(updates['release'][namespace]['version'], "This version is not found. Maybe it is not recorded.")
    elif version == WILL: 
        out_obj = open_dict.get(WILL, "This version is not found. Maybe it is not recorded.")
    else: 
        out_obj = open_dict.get(str(version), "This version is not found. Maybe it is not recorded.")
    
    print(out_obj)
    return out_obj

def get_version_update_time(namespace:str, version: str): 
    '''Get the version update time.'''
    try:
        open_dict = updates['release'][namespace]['update_time']
    except KeyError:
        raise ValueError('This namespace not found.')

    if version == ALL: 
        out_obj = open_dict
    elif version == NEW: 
        out_obj = open_dict.get(updates['release'][namespace]['version'], "This version is not found. Maybe it is not recorded.")
    elif version == WILL: 
        raise ValueError('`get_version_update_time` cannot get will update time.')
    else: 
        out_obj = open_dict.get(str(version), "This version is not found. Maybe it is not recorded.")
    
    print(out_obj)
    return out_obj

def get_will(namespace:str): 
    '''Get the will update doc.'''
    return get_update(namespace, WILL)

def get_version(namespace:str):
    '''Get the version.'''
    return updates['release'][namespace]['version']

def get_pre_version():
    '''Get the pre version.'''
    return updates['pre-release']['version']

def get_news_update_time(namespace:str): 
    '''Get the new update time.'''
    return get_version_update_time(namespace, NEW)

def get_new(namespace:str): 
    '''Get the new update doc.'''
    return get_update(namespace, NEW)

def get_all(namespace:str): 
    '''Get the all update doc.'''
    return get_update(namespace, ALL)

def get_will(namespace:str): 
    '''Get the will update doc.'''
    return get_update(namespace, WILL)

def get_pre_update(version: str): 
    '''Get the pre-release version update doc.'''
    try:
        open_dict = updates['pre-release']['update_info']
    except KeyError:
        raise ValueError('This namespace not found.')

    if version == ALL: 
        out_obj = open_dict
    elif version == NEW: 
        out_obj = open_dict.get(updates['pre-release']['version'], "This version is not found. Maybe it is not recorded.")
    elif version == WILL: 
        out_obj = open_dict.get(WILL, "This version is not found. Maybe it is not recorded.")
    else: 
        out_obj = open_dict.get(str(version), "This version is not found. Maybe it is not recorded.")

    print(out_obj)
    return out_obj

def get_pre_version_update_time(version: str): 
    '''Get the pre-release version update time.'''
    try:
        open_dict = updates['pre-release']['update_time']
    except KeyError:
        raise ValueError('This namespace not found.')

    if version == NEW: 
        out_obj = open_dict
    elif version == NEW: 
        out_obj = open_dict.get(updates['pre-release']['version'], "This version is not found. Maybe it is not recorded.")
    elif version == WILL: 
        raise ValueError('`get_version_update_time` cannot get will update time.')
    else: 
        out_obj = open_dict.get(str(version), "This version is not found. Maybe it is not recorded.")
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

def open_doc(doc_name:str):
    raise NotImplementedError("Document is not completed.")

__version__ = get_version("main")