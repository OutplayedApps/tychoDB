# -*- coding: utf-8 -*-
import os
import re
import json

categoryList = {
    "OTHER": -1,
    "EARTH SCIENCE": 0,
    "EARTH AND SPACE": 0,
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
    r"(TOSS\-UP|TOSSUP|TOSS UP)\s*"
    r"(?P<questionNum>\d{1,2})[\.\)]\s*(?P<category>[A-Z ]+)\s*"
    r"(?i)(Short Answer|Multiple Choice)\s*(?P<tossupQ>[\S\s]*)"
    r"ANSWER\:(?P<tossupA>[\w ]*)"

    r"\s*BONUS\s*"
    r"(?P<questionNumBonus>\d{1,2})[\.\)]\s*(?P<categoryBonus>[A-Z ]+)\s*"
    r"(?i)(Short Answer|Multiple Choice)\s*(?P<bonusQ>[\S\s]*)"
    r"ANSWER\:(?P<bonusA>[\w\)\. ]*)\s*"
)

replaceString = r"""
{{
    "category": {categoryId},
    "questionNum": {questionNum},
    "tossupQ": "{tossupQ}",
    "tossupA": "{tossupA}",
    "bonusQ": "{bonusQ}",
    "bonusA": "{bonusA}"
}},
"""

def format(string):
    return string.strip().encode("string_escape")

def getCategoryId(category):

    category = category.strip()
    if category in categoryList:
        return categoryList[category]
    else:
        print "can't find category: " + category
        #raise ValueError("can\'t find cat" + category)
        return categoryList["OTHER"]

def parse(text):
    text = """


TOSS UP



1. MATH  Short Answer  Pablo walks 4 miles north, 6 miles east, and then 2 miles north again. In simplest form, how many miles is he from his starting point?



ANSWER: 6



BONUS



1. MATH  Short Answer  Evaluate the limit as x approaches infinity of x times the quantity negative 1 plus e to the 1 over x.



ANSWER: 1



TOSS UP



2. CHEMISTRY  Multiple Choice  Which of the following is NOT a characteristic of amines?



W) A fully protonated amine is called an ammonium ion

X) Amines can function as Brønsted bases

Y) The VSEPR geometry of the nitrogen atom is trigonal planar

Z) Amines can be a hydrogen bond acceptor



ANSWER: Y) The VSEPR geometry of the nitrogen atom is trigonal planar



BONUS



2. CHEMISTRY  Multiple Choice  Of the following elements in their monatomic gaseous states, which has the lowest electron affinity?



W) BoronX) CarbonY) NitrogenZ) OxygenANSWER: Y) NITROGEN


    """
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
    return jsonstring
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
    break