#!/bin/bash

RUN_PYTHON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertSquadPython; print(getBertSquadPython())')
BERT_PRETRAINED=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertPretrainedModel; print(getBertPretrainedModel())')
BERT_INPUT_JSON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertInputJson; print(getBertInputJson())')
BERT_OUTPUT=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertOutput; print(getBertOutput())')
BERT_INIT_CKPT=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertInitCkpt; print(getBertInitCkpt())')
BERT_LOG=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertLog; print(getBertLog())')

/usr/bin/python3 ${RUN_PYTHON} --bert_config_file=${BERT_PRETRAINED}/bert_config.json --vocab_file=${BERT_PRETRAINED}/vocab.txt --do_predict=True --predict_file=${BERT_INPUT_JSON} --do_lower_case=false --num_train_epochs=3.0 --max_seq_length=256 --train_batch_size=16 --learning_rate=2e-5 --output_dir=${BERT_OUTPUT} --init_checkpoint=${BERT_INIT_CKPT} --query_text=$1 > ${BERT_LOG}

