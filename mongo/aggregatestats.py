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

def getEntryFileName(entry):
	return "%s-%s-%s" % (entry["vendorNum"], entry["setNum"], entry["packetNum"])

client = MongoClient(DB_MONGO_CONN_STRING)
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

def writeMetadata():
	"""
	Writes the metadata file from summary query.
	"""
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
	updateMetadataLabels(metadata)
	file.write(json.dumps(metadata, indent=2));
	file.close();
	copy_labels_file()
	
def writeToFiles(vendorsToSkip=[]):
	"""
	Writes to local files (for use in the app).
	"""
	print "writing to files..."
	for element in summary:
		# entry is: packetNum, vendorNum, setNum identifier.
		entry = element["_id"]
		if entry["vendorNum"] in vendorsToSkip:
			continue
		print str(element)
		file = open('./%s/%s.json' % (OUTPUT_DIR, getEntryFileName(entry)), 'w')
		questionsInSet = questions.find(entry)
		file.write(dumps(questionsInSet, indent=2))

		sleep(0.05)
		file.close();

def convertTypes(vendorsToSkip=[]):
	"""
	Converts setNum, questionNum all to integers.
	"""
	for element in summary:
		# entry is: packetNum, vendorNum, setNum identifier.
		entry = element["_id"]
		# print str(element)
		if entry["vendorNum"] in vendorsToSkip:
			continue
		questionsInSet = questions.find(entry)
		for question in questionsInSet:
			for attr in ["setNum", "questionNum", "packetNum"]:
				if attr in question and isinstance(question[attr], basestring):
					questions.update_one({"_id": question["_id"]}, {"$set": {attr: int(question[attr])}})
					print 'updating one: ' + str(question["_id"]) + question["tossupQ"][1:10]
					sleep(0.05)


writeMetadata()
writeToFiles(["DOE-MS","DOE-HS"])
# writeToFiles()
# convertTypes()