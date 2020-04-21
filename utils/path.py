# coding=utf-8

import os

## DIRECTORY
BERT_HOME = "/home/taejoon1kim/BERT/my_bert"
BERT_PRETRAINED_MODEL = "/home/taejoon1kim/BERT/pretrained_files"

## CACHE
DOWNLOAD_CACHE_PATH = f"{BERT_HOME}/download_cache/"
BERT_CACHE_PATH = f"{BERT_HOME}/bert_cache/"
CACHE_POSTFIX = ".pkl"

## OUTPUT
BERT_OUTPUT = f"{BERT_HOME}/output"
BERT_INPUT_JSON = f"{BERT_OUTPUT}/test_input.json"
BERT_SEARCH_JSON = f"{BERT_OUTPUT}/search_result.json"
BERT_PREDICTIONS_JSON = f"{BERT_OUTPUT}/predictions.json"
BERT_LOG = f"{BERT_OUTPUT}/test_log.txt"

## RUN CONF
BERT_SQUAD_PYTHON = f"{BERT_HOME}/run_squad.py"
BERT_INIT_CKPT = f"{BERT_HOME}/output-KorQUaD_0305-output/model.ckpt-11326"


def getBertInputJson():
    return BERT_INPUT_JSON

def getBertSearchJson():
    return BERT_SEARCH_JSON

def getBertPredictionsJson():
    return BERT_PREDICTIONS_JSON

def getBertSquadPython():
    return BERT_SQUAD_PYTHON

def getBertPretrainedModel():
    return BERT_PRETRAINED_MODEL

def getBertOutput():
    return BERT_OUTPUT

def getBertInitCkpt():
    return BERT_INIT_CKPT

def getBertLog():
    return BERT_LOG
