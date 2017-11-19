import json
from pymongo import MongoClient
import urllib
from bson.son import SON
import pprint
import os
from bson.json_util import dumps

def getEntryFileName(entry):
	return "%s-%s-%s" % (entry["vendorNum"], entry["setNum"], entry["packetNum"])

user = 'tycho'
pwd = 'tych0@@@'
user = urllib.quote_plus(user)
pwd = urllib.quote_plus(pwd)
client = MongoClient('mongodb://'+user+':'+pwd+'@ds113566.mlab.com:13566/tycho')
questions = client.tycho.questions
OUTPUT_DIR = 'output'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

pipeline = [
     {"$group":
     	{"_id": {"vendorNum": "$vendorNum", "setNum": "$setNum", "packetNum": "$packetNum" },
     	"count": {"$sum": 1}
     }},
     {"$sort": SON([("count", -1), ("_id", -1)])}
]

summary = list(questions.aggregate(pipeline))

metadata = {}

for element in summary:
	entry = element["_id"]
	if not entry["vendorNum"] in metadata:
		metadata[entry["vendorNum"]] = {}
	if not entry["setNum"] in metadata[entry["vendorNum"]]:
		metadata[entry["vendorNum"]][entry["setNum"]] = {}
	if not entry["packetNum"] in metadata[entry["vendorNum"]][entry["setNum"]]:
		# always called
		metadata[entry["vendorNum"]][entry["setNum"]][entry["packetNum"]] = {"numQuestions": element["count"],
			"fileName": getEntryFileName(entry)}

print "writing metadata..."
file = open('./%s/metadata.json' % (OUTPUT_DIR), 'w')
file.write(json.dumps(metadata, indent=2));
file.close();


print "writing to files..."
for element in summary:
	entry = element["_id"]
	print entry
	file = open('./%s/%s.json' % (OUTPUT_DIR, getEntryFileName(entry)), 'w')
	file.write(dumps(questions.find(entry), indent=2));
	file.close();