import json
from pymongo import MongoClient
import urllib
from bson.son import SON
import pprint
import os
from bson.json_util import dumps
from time import sleep
from shutil import copyfile
from secret import DB_MONGO_CONN_STRING
from datetime import datetime

def getEntryFileName(entry):
	return "%s-%s-%s" % (entry["vendorNum"], entry["setNum"], entry["packetNum"])

client = MongoClient(DB_MONGO_CONN_STRING)
questions = client.tycho.questions
metadataCollection = client.tycho.metadata
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
print json.dumps(summary)

metadata = {}

def merge(source, destination):
	"""
	From https://stackoverflow.com/questions/20656135/python-deep-merge-dictionary-data
	"""
	for key, value in source.items():
		if isinstance(value, dict):
			# get node or create one
			try: 
				key = int(key)
			except ValueError:
				pass
			node = destination.setdefault(key, {})
			merge(value, node)
		else:
			destination[key] = value

	return destination

def updateMetadataLabels(metadata):
	"""
	Updates metadata's labels based on information in labels.json
	"""
	file = open('./labels.json', 'r')
	labels = json.loads(file.read())
	merge(labels, metadata)
	file.close()

def copy_labels_file():
	"""
	Copies labels file from current directory to output directory.
	Not used in the app, but just good to have all the data be included in the app anyways.
	"""
	copyfile('./labels.json', './%s/labels.json' % (OUTPUT_DIR))

def isQuestion(entry, vendorsToSkip=[]):
	return "vendorNum" in entry and not (entry["vendorNum"] in vendorsToSkip)

def writeMetadata(vendorsToSkip = []):
	"""
	Writes the metadata file from summary query.
	"""
	for element in summary:
		entry = element["_id"]
		if not isQuestion(entry, vendorsToSkip): continue
		if "setNum" in entry: entry["setNum"] = int(entry["setNum"])
		if "packetNum" in entry: entry["packetNum"] = int(entry["packetNum"])
		if "questionNum" in entry: entry["questionNum"] = int(entry["questionNum"])
		if not entry["vendorNum"] in metadata:
			metadata[entry["vendorNum"]] = {}
		if not entry["setNum"] in metadata[entry["vendorNum"]]:
			metadata[entry["vendorNum"]][entry["setNum"]] = {}
		if not entry["packetNum"] in metadata[entry["vendorNum"]][entry["setNum"]]:
			# always called
			metadata[entry["vendorNum"]][entry["setNum"]][entry["packetNum"]] = {"numQuestions": element["count"],
				"fileName": getEntryFileName(entry)}

	# print "writing metadata..."
	file = open('./%s/metadata.json' % (OUTPUT_DIR), 'w')
	updateMetadataLabels(metadata)
	dateNow = datetime.now().isoformat()
	metadataCollection.update_one({"type": "metadata"}, {"$set": {"value": json.loads(json.dumps(metadata)), "date_modified": dateNow }}, upsert=True)
	metadata["metadata"] = {"date_modified": dateNow};
	file.write(json.dumps(metadata, indent=2));
	file.close();
	copy_labels_file()
	
def writeToFiles(vendorsToSkip=[], separateFiles = False):
	"""
	Writes to local files (for use in the app).
	"""
	print "writing to files..."
	everything = {}
	for element in summary:
		# entry is: packetNum, vendorNum, setNum identifier.
		entry = element["_id"]
		if not isQuestion(entry, vendorsToSkip): continue
		entryFileName = getEntryFileName(entry)
		#print str(entry['tossupQ'])
		questionsInSet = questions.find(entry, {"tossupQ": 1, "tossupA": 1, "bonusQ": 1, "bonusA": 1, "questionNum": 1, "category": 1})
		if separateFiles:
			file = open('./%s/%s.json' % (OUTPUT_DIR, entryFileName), 'w')
			file.write(dumps(questionsInSet, indent=2))
			file.close();
			sleep(0.05)
		else:
			everything[entryFileName] = questionsInSet
	if not separateFiles:
		file = open('./%s/all.json' % (OUTPUT_DIR, ), 'w')
		questionsInSet = questions.find(entry)
		file.write(dumps(everything))
		file.close();

def convertTypes(vendorsToSkip=[]):
	"""
	Converts setNum, questionNum all to integers.
	"""
	for element in summary:
		# entry is: packetNum, vendorNum, setNum identifier.
		entry = element["_id"]
		if not isQuestion(entry, vendorsToSkip): continue
		questionsInSet = questions.find(entry)
		for question in questionsInSet:
			for attr in ["setNum", "questionNum", "packetNum"]:
				if attr in question and isinstance(question[attr], basestring):
					questions.update_one({"_id": question["_id"]}, {"$set": {attr: int(question[attr])}})
					print 'updating one: ' + str(question["_id"]) + question["tossupQ"][1:10]
					sleep(0.05)


writeMetadata()
# writeToFiles(["DOE-MS","DOE-HS"])
writeToFiles()
# convertTypes()