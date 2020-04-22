# coding=utf-8

import sys, getopt
import urllib
import requests
import requests_cache
import re
import time
from bs4 import BeautifulSoup
from requests import Session

sys.path.append("/home/taejoon1kim/BERT/my_bert")

from utils.cacheUtils import cacheExist, writeCache, readCache, getDownloadCachePath
from utils.path import BERT_INPUT_JSON, BERT_SEARCH_JSON

def preprocessor(text):
    if "감독" in text:
        return text[0:text.find("감독")]
    elif "등장인물" in text:
        return text[0:text.find("등장인물")]
    elif "누구야" in text:
        return text[0:text.find("누구야")]
    elif "알려줘" in text:
        return text[0:text.find("알려줘")]
    elif "보여줘" in text:
        return text[0:text.find("보여줘")]
    elif "찾아줘" in text:
        return text[0:text.find("찾아줘")]
    elif "언제야" in text:
        return text[0:text.find("언제")]
    elif "어디" in text:
        return text[0:text.find("어디")]
    elif "뭐야" in text:
        return text[0:text.find("뭐야")]
    else :
        return text

def checkQType(text):
    global Q_TYPE
    if "감독" in text or "어디서" in text or "언제" in text or "뭐야" in text:
        Q_TYPE = 2
    elif "누구야" in text:
        Q_TYPE = 1
    else:
        Q_TYPE = 3
    SEARCH_RESULT['Q_TYPE'] = Q_TYPE
    print("QUESTION TYPE : ", Q_TYPE)

WIKI_URL = "wikipedia.org"
YOUTUBE_URL = "youtube.com/channel"

NO_RESULT = "no_result"

SEARCH_RESULT = {
        "WIKI" : {"title" : f"{NO_RESULT}", "link" : f"{NO_RESULT}"},
        "FIRST" : {"title" : f"{NO_RESULT}", "link" : f"{NO_RESULT}"},
        "YOUTUBE" : {"title" : f"{NO_RESULT}", "link" : f"{NO_RESULT}"},
        "test_input.json" : f"{NO_RESULT}",
        "search_result.json" : f"{NO_RESULT}",
        "Q_TYPE" : f"{NO_RESULT}"
        }


def downloadURL(URL):
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

    headers = {"user-agent" : USER_AGENT}
    #headers = {"user-agent" : USER_AGENT, "cache-contorl" : "public,max-age=3600"}
    #headers = {"user-agent" : USER_AGENT, "cache-contorl" : "no-cache"}
    #s = Session()
    #s.headers.update(headers)
    resp = requests.get(URL, headers=headers)
    #resp = s.get(URL)

    results = [{"title" : f"{NO_RESULT}", "link" : f"{NO_RESULT}"}]
    print(resp.status_code)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "lxml")

        results = []
        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                item = {
                    "title": title,
                    "link": link
                }
                results.append(item)
                #print(link)
                global SEARCH_RESULT
                if link.find(WIKI_URL) != -1 and SEARCH_RESULT['WIKI']['link'] == NO_RESULT:
                    SEARCH_RESULT['WIKI']['title'] = title
                    SEARCH_RESULT['WIKI']['link'] = link
                elif link.find(YOUTUBE_URL) != -1 and SEARCH_RESULT['YOUTUBE']['link'] == NO_RESULT:
                    SEARCH_RESULT['YOUTUBE']['title'] = title
                    SEARCH_RESULT['YOUTUBE']['link'] = link
                
                if SEARCH_RESULT['WIKI']['link'] != NO_RESULT and SEARCH_RESULT['YOUTUBE']['link'] != NO_RESULT:
                    break
        SEARCH_RESULT['FIRST']['title'] = results[0].get('title')
        SEARCH_RESULT['FIRST']['link'] = results[0].get('link')
    else:
        SEARCH_RESULT['FIRST']['title'] = f"resp.status_code {resp.status_code}"
    return results
    
def download(text):
    global cache
    cache = getDownloadCachePath(text)
    global start, Q_TYPE
    init_start = time.time()
    start = time.time()
    requests_cache.install_cache('/home/taejoon1kim/BERT/my_bert/download_cache')

    #if cacheExist(cache) == False:
    if True:
    
        checkQType(text)
        query_text = preprocessor(text)


        ## 1st SEARCH
        query = query_text
        query = query.replace(' ', '+')
        if Q_TYPE <= 2:
            URL = f"https://google.com/search?q={query} site:wikipedia.org"
        else :
            URL = f"https://google.com/search?q={query}"
        print(URL)
        downloadURL(URL)
        printTime("1st Search Time")


        pWithoutTag = f"{NO_RESULT}"
        imgTag = f"{NO_RESULT}"
        ## 2nd SEARCH
        if SEARCH_RESULT['WIKI']['title'] == NO_RESULT and Q_TYPE > 2:
            URL = f"https://google.com/search?q={query} site:wikipedia.org"
            downloadURL(URL)
        if SEARCH_RESULT['WIKI']['title'] == NO_RESULT:
            pWithoutTag = "위키피디아가 없네요. 링크를 열어보세요"
        else:
            resp = requests.get(SEARCH_RESULT['WIKI']['link'])
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, "lxml")
    
                p = soup.find('p')
                pWithoutTag = re.sub('<.+?>', '', str(p), 0).strip()
                pWithoutTag = re.sub('"', '', str(pWithoutTag), 0).strip()
                pWithoutTag = re.sub('\n', ' ', str(pWithoutTag), 0).strip()

                imgTag = "http:" + soup.find('a', {'class':'image'}).find('img')['src']


        ## GENERATE BERT INPUT
        JSON_1 = "{\"version\":\"mytest_dev\",\"data\":[{\"paragraphs\":[{\"qas\":[{\"answers\":[{\"text\":\"테스트\",\"answer_start\":0}],\"id\":\"1-1\",\"question\":\"테스트\"}],\"context\":\""
        JSON_2 = "\"}],\"title\":\"테스트\"}]}"
        FULL_JSON = JSON_1 + pWithoutTag + JSON_2
        writeJson(FULL_JSON, BERT_INPUT_JSON)
        printTime("2nd Search Time")
        SEARCH_RESULT['test_input.json'] = FULL_JSON
    

        ## GENERATE SEARCH RESULT
        FULL_JSON = "{\"google\":[{\"title\":\"" + SEARCH_RESULT['FIRST']['title'] + "\",\"link\":\"" + SEARCH_RESULT['FIRST']['link'] + "\"}],\"wiki\":[{\"title\":\"" + SEARCH_RESULT['WIKI']['title'] + "\",\"link\":\"" + SEARCH_RESULT['WIKI']['link'] + "\"}],\"youtube\":[{\"title\":\"" + SEARCH_RESULT['YOUTUBE']['title'] + "\",\"link\":\"" + SEARCH_RESULT['YOUTUBE']['link'] + "\"}],\"Q_TYPE\":\"" + str(Q_TYPE) + "\",\"IMG_SRC\":\"" + str(imgTag) + "\"}"
        writeJson(FULL_JSON, BERT_SEARCH_JSON)
        SEARCH_RESULT['search_result.json'] = FULL_JSON
        writeCache(cache, SEARCH_RESULT)
    else:
        CACHE_RESULT = readCache(cache)
        writeJson(CACHE_RESULT['test_input.json'], BERT_INPUT_JSON)
        writeJson(CACHE_RESULT['search_result.json'], BERT_SEARCH_JSON)
        Q_TYPE = CACHE_RESULT['Q_TYPE']

    print(f"[SEARCH] Total time : {format(time.time() - init_start, '0.5f')}")

    return Q_TYPE


def writeJson(json, filePath):
    f = open(filePath, 'w')
    f.write(json)
    f.close()

def printTime(text):
    global start
    print(f"[SEARCH] {text} : {format(time.time() - start, '0.5f')}")
    start = time.time()

def main(argv):
    download(argv[1])

if __name__ == "__main__":
    main(sys.argv)
