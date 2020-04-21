#!/bin/bash

RESULT_FILE="result/result_"$(date "+%Y-%m-%d_%H:%M:%S")".txt"
echo -e "TEXT\tSEARCH TIME\tPREDICTION TIME\tPREDICTION\tQ_TYPE\tPARAGRAPH\tGOOGLE TITLE\tGOOGLE LINK\tWIKI TITLE\tWIKI LINK\tYOUTUBE TITLE\tYOUTUBE LINK\tIMG SRC" > ${RESULT_FILE}

let i=1
while IFS=, read -u12 -r line
do
	if [ $i -eq 1 ];then
		ip=$line
	elif [ $i -eq 2 ];then
		port=$line
	else
		let j=1
		while [ $j -lt 3 ]
		do
			ssh -p $port root@$ip "luna-send -n 1 -f luna://com.webos.service.voiceconductor/recognizeIntentByText '{\"text\":\"${line}\", \"runVoiceUi\":true, \"language\":\"ko-KR\"}'"
			SEARCH_TIME=$(grep '\[SEARCH\] Total' /home/taejoon1kim/BERT/my_bert/output/test_log.txt)
			PREDICTION_TIME=$(grep '\[BERT Model\] Total' /home/taejoon1kim/BERT/my_bert/output/test_log.txt)
			PREDICTION=$(jq '."1-1"' /home/taejoon1kim/BERT/my_bert/output/predictions.json)
			Q_TYPE=$(jq '.Q_TYPE' /home/taejoon1kim/BERT/my_bert/output/search_result.json)
			GOOGLE_T=$(jq '.google[0].title' /home/taejoon1kim/BERT/my_bert/output/search_result.json)
			GOOGLE_L=$(jq '.google[0].link' /home/taejoon1kim/BERT/my_bert/output/search_result.json)
			WIKI_T=$(jq '.wiki[0].title' /home/taejoon1kim/BERT/my_bert/output/search_result.json)
			WIKI_L=$(jq '.wiki[0].link' /home/taejoon1kim/BERT/my_bert/output/search_result.json)
			YOUTUBE_T=$(jq '.youtube[0].title' /home/taejoon1kim/BERT/my_bert/output/search_result.json)
			YOUTUBE_L=$(jq '.youtube[0].link' /home/taejoon1kim/BERT/my_bert/output/search_result.json)
			IMG_SRC=$(jq '.IMG_SRC' /home/taejoon1kim/BERT/my_bert/output/search_result.json)
			PARAGRAPH=$(jq '.data[0].paragraphs[0].context' /home/taejoon1kim/BERT/my_bert/output/test_input.json)
			echo -e "$line\t${SEARCH_TIME: (-7)}\t${PREDICTION_TIME: (-7)}\t${PREDICTION//\"/}\t${Q_TYPE//\"/}\t${PARAGRAPH//\"/}\t${GOOGLE_T//\"/}\t${GOOGLE_L//\"/}\t${WIKI_T//\"/}\t${WIKI_L//\"/}\t${YOUTUBE_T//\"/}\t${YOUTUBE_L//\"/}\t${IMG_SRC//\"/}" >> ${RESULT_FILE}
			let j++
		done
	fi
	let i++
done 12< config.txt
