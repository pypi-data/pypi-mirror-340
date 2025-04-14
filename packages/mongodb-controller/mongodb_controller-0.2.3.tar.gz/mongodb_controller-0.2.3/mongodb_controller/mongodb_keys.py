from .mongodb_collections import (
    COLLECTION_2110,
    COLLECTION_2160,
    COLLECTION_2205,
    COLLECTION_2205_SNAPSHOT,
    COLLECTION_8186,
    COLLECTION_BBG_TIMESERIES,
    COLLECTION_ESAFE
)

def get_keys_of_collection(collection):
    return list(collection.find_one().keys())

def get_keys_menu2110():
    return get_keys_of_collection(COLLECTION_2110)

def get_keys_menu2160():
    return get_keys_of_collection(COLLECTION_2160)

def get_keys_menu2205():
    return get_keys_of_collection(COLLECTION_2205)

def get_keys_menu2205_snapshot():
    return get_keys_of_collection(COLLECTION_2205_SNAPSHOT)

def get_keys_menu8186():
    return get_keys_of_collection(COLLECTION_8186)

def get_keys_bbg_timeseries():
    return get_keys_of_collection(COLLECTION_BBG_TIMESERIES)

def get_keys_esafe():
    return get_keys_of_collection(COLLECTION_ESAFE)
