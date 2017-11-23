import json
from pymongo import MongoClient
import urllib
from datetime import datetime
from secret import DB_MONGO_CONN_STRING

#client = MongoClient(DB_MONGO_CONN_STRING)
questions = client.tycho.questions

with open('import/data.json') as json_data:
    d = json.load(json_data)
    for entry in d:
    	if (hasattr(entry, "questionNum")):
    		entry.questionNum = int(entry.questionNum)
        entry['vendorNum'] = 'SAMPLE-DE-HS'
    	entry['setNum'] = 1
        entry['packetNum'] = 2
        entry['date_modified'] = datetime.now().isoformat()
        entry['date_created'] = datetime.now().isoformat()
    print str(d)
    questions.insert_many(d)
print "done"