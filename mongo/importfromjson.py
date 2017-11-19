import json
from pymongo import MongoClient
import urllib
user = 'tycho'
pwd = 'tych0@@@'
user = urllib.quote_plus(user)
pwd = urllib.quote_plus(pwd)
#client = MongoClient('mongodb://'+user+':'+pwd+'@ds113566.mlab.com:13566/tycho')
questions = client.tycho.questions

with open('data.json') as json_data:
    d = json.load(json_data)
    for entry in d:
    	if (hasattr(entry, "questionNum")):
    		entry.questionNum = int(entry.questionNum)
    questions.insert_many(d)
print "done"