#!/bin/bash

JSON="NONE"
XPATH="NONE"
BERT_HOME="abc"
if [ "$1" == "description" ];then
	JSON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertInputJson; print(getBertInputJson())')
	XPATH='.data[0].paragraphs[0].context'
elif [ "$1" == "google_link" ];then
	JSON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertSearchJson; print(getBertSearchJson())')
	XPATH='.google[0].link'
elif [ "$1" == "google_title" ];then
	JSON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertSearchJson; print(getBertSearchJson())')
	XPATH='.google[0].title'
elif [ "$1" == "imgSrc" ];then
	JSON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertSearchJson; print(getBertSearchJson())')
	XPATH='.IMG_SRC'
elif [ "$1" == "q_type" ];then
	JSON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertSearchJson; print(getBertSearchJson())')
	XPATH='.Q_TYPE'
elif [ "$1" == "wiki_link" ];then
	JSON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertSearchJson; print(getBertSearchJson())')
	XPATH='.wiki[0].link'
elif [ "$1" == "wiki_title" ];then
	JSON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertSearchJson; print(getBertSearchJson())')
	XPATH='.wiki[0].title'
elif [ "$1" == "youtube_link" ];then
	JSON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertSearchJson; print(getBertSearchJson())')
	XPATH='.youtube[0].link'
elif [ "$1" == "youtube_title" ];then
	JSON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertSearchJson; print(getBertSearchJson())')
	XPATH='.youtube[0].title'
elif [ "$1" == "predictions" ];then
	JSON=$(/usr/bin/python3 -c 'import sys;sys.path.append("/home/taejoon1kim/BERT/my_bert");from utils.path import getBertPredictionsJson; print(getBertPredictionsJson())')
	XPATH='."1-1"'
fi
/usr/bin/jq $XPATH $JSON
