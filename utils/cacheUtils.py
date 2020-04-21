# coding=utf-8

import os.path
import pickle
import sys

sys.path.append("/home/taejoon1kim/BERT/my_bert")

from utils.path import DOWNLOAD_CACHE_PATH, BERT_CACHE_PATH, CACHE_POSTFIX

def cacheExist(cache):
    if os.path.isfile(cache):
        return True
    return False

def writeCache(cache, json):
    with open(cache, 'wb') as f:
        return pickle.dump(json, f)

def readCache(cache):
    with open(cache, 'rb') as f:
        return pickle.load(f)

def getDownloadCachePath(text):
    return '{}{}{}'.format(DOWNLOAD_CACHE_PATH, text.replace('/', '_').replace(' ', '_'), CACHE_POSTFIX)

def getBertCachePath(text):
    return '{}{}{}'.format(BERT_CACHE_PATH, text.replace('/', '_').replace(' ', '_'), CACHE_POSTFIX)
