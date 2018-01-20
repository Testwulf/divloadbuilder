'''A file-based cache controller'''


import os
import pickle


CACHE_ROOT = 'cache'
if not os.path.exists(CACHE_ROOT):
    os.mkdir(CACHE_ROOT)


def exists(name, target=CACHE_ROOT):
    '''Returns True if a cache exists, or False otherwise'''
    full_path = '%s/%s' % (target, name)
    return os.path.exists(full_path)


def get(name, target=CACHE_ROOT):
    '''Get the object in the named cache'''
    save_object = None
    full_path = '%s/%s' % (target, name)
    with open(full_path, 'rb') as input_file:
        save_object = pickle.load(input_file)
    return save_object


def get_sub(sub_cache):
    '''Returns the path to a given sub-cache'''
    sub_path = '{}/{}'.format(CACHE_ROOT, sub_cache)
    return sub_path


def put(save_object, name, target=CACHE_ROOT):
    '''Put a given object into the named cache'''
    full_path = '%s/%s' % (target, name)
    with open(full_path, 'wb') as output_file:
        pickle.dump(save_object, output_file, pickle.HIGHEST_PROTOCOL)


def register(sub_cache):
    '''Registers a new sub-cache'''
    new_path = '{}/{}'.format(CACHE_ROOT, sub_cache)
    if not os.path.exists(new_path):
        os.mkdir(new_path)
