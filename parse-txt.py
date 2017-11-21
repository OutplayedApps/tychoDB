# -*- coding: utf-8 -*-
import os
import re
import json

categoryList = {
    "OTHER": -1,
    "EARTH SCIENCE": 0,
    "EARTH AND SPACE": 0,
    "EARTH AND SPACE SCIENCE": 0,
    "ESSC": 0,
    "ASTRONOMY": 0,
    "BIOLOGY": 1,
    "CHEMISTRY": 2,
    "PHYSICS": 3,
    "MATHEMATICS": 4,
    "MATH": 4,
    "ENERGY": 5,
    "GENERAL SCIENCE": 6,
    "COMPUTER SCIENCE": 7
};

searchString = (
    r"(?i)(TOSS\-UP|TOSSUP|TOSS\s*UP)\s*"
    r"(?P<questionNum>\d{1,2})[\.\)\:]\s*(?P<category>[A-Za-z ]+)\:?\s*"
    r"(?i)((Short Answer|Multiple Choice)\:?)\s*(?P<tossupQ>[\S\s]*?)"
    r"ANSWER\:(?P<tossupA>[\S\s]*?)"

    r"\s*(?i)(BONUS)\s*"
    r"(?P<questionNumBonus>\d{1,2})[\.\)\:]\s*(?P<categoryBonus>[A-Za-z ]+)\:?\s*"
    r"(?i)((Short Answer|Multiple Choice)\:?)\s*(?P<bonusQ>[\S\s]*?)"
    r"ANSWER\:(?P<bonusA>[\S\s]*?)(?=TOSS)"
)

replaceString = r"""
{{
    "category": {categoryId},
    "questionNum": {questionNum},
    "tossupQ": "{tossupQ}",
    "tossupA": "{tossupA}",
    "bonusQ": "{bonusQ}",
    "bonusA": "{bonusA}"
}},"""

def format(string):
    return string.strip().replace("\n","\\n")

def getCategoryId(category):

    category = category.strip().upper()
    if category in categoryList:
        return categoryList[category]
    else:
        #print "can't find category: " + category
        raise ValueError("can\'t find cat" + category)
        return categoryList["OTHER"]

def parse(text):
    text += "TOSS-UP"
    jsonstring = re.sub(
        searchString,
        lambda m: replaceString.format(
            categoryId=getCategoryId(m.group('category')),
            questionNum = format(m.group('questionNum')),
            tossupQ=format(m.group('tossupQ').strip()),
            tossupA=format(m.group('tossupA').strip()),
            bonusQ=format(m.group('bonusQ').strip()),
            bonusA=format(m.group('bonusA'))
            ),
        text
        )
    jsonstring = jsonstring[:-7] # remove TOSS-UP
    jsonstring = jsonstring[:-1] # remove ,
    jsonstring = re.sub("\\xe2\\x80\\x99", "'", jsonstring);
    return "[" + jsonstring + "]"
    #return json.loads("[" + jsonstring + "]")

input_folder = "txt"
output_folder = "txtoutput"
dir_path = os.path.dirname(os.path.realpath(__file__))
input_full_path = dir_path + "\\" + input_folder + "\\"

for fn in os.listdir(input_full_path):
    with open(input_full_path + fn) as f:
        text = f.read()
        text = parse(text)
        print text
        with open(output_folder + "\\" +  fn + ".json", "w") as f:
            f.write(text)
    