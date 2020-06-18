from itertools import chain
import json
import pymongo

with open('/Users/minwater/Downloads/pyTrendyWord_DataGenerator-master/result/NLP/2020-06-08/Economy_news.arirang.json', 'r') as f:
    json_data = json.load(f)

RE_JSON = {
    "RAWDATAS" :
        [
        ]
}

# word/tag
# 0 - word 1 - tag

word = [i.split('/')[0] for i in json_data["context"]]
tag =  [i.split('/') for i in json_data["context"]]

for i,value in enumerate(tag) :
    if i == 10 :
        break
    APPEND_JSON = {
        "word" : value[0],
        "POS-tag" : value[1],
        "subject" : json_data["subject"],
        "info" : []
    }

    APPEND_JSON_INFO = {
        "year" : json_data["crawlingDate"].split('-')[0],
        "month" : json_data["crawlingDate"].split('-')[1],
        "date" : json_data["crawlingDate"].split('-')[2],
        "count" : word.count(value[0])
    }

    APPEND_JSON["info"].append(APPEND_JSON_INFO)
    RE_JSON["RAWDATAS"].append(APPEND_JSON)

print(RE_JSON)

# 디비에 넣기
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["T_RAWDATAS"]

mycol.insert_one(RE_JSON)
