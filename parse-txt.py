import os
import re

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
    r"(?P<questionNum>\d\d)[\.\)].*(?P<category>[A-Z ]+)"
    r"(?i)(Short Answer|Multiple Choice) (?P<tossupQ>[A-Za-z*])"
)

replaceString = r"""
{{
    "category": {categoryId},
    "questionNum": {questionNum},
    "tossupQ": {tossupQ},
}},
"""

def getCategoryId(category):

    category = category.strip()
    if category in categoryList:
        return categoryList[category]
    else:
        print "can't find category: " + category
        return categoryList["OTHER"]

def parse(text):
    return re.sub(
        searchString,
        lambda m: replaceString.format(
            categoryId=getCategoryId(m.group('category')),
            questionNum = m.group('questionNum'),
            tossupQ=m.group('tossupQ'),
            ),
        text
        )

input_folder = "txt"
output_folder = "txtoutput"
dir_path = os.path.dirname(os.path.realpath(__file__))
input_full_path = dir_path + "\\" + input_folder + "\\"

for fn in os.listdir(input_full_path):
    print fn
    with open(input_full_path + fn) as f:
        text = f.read()
        text = parse(text)
        print text
    break