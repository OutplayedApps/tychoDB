Workflow:
- Put docx files in "docx files input" directory.
- Run ```node convert-to-txt.js```; output text files will be in "txt" directory.
- Put text files in "txt" folders, and fix them manually as below.
- Run ```python parse-txt.py```. Output (JSON) will be in txtoutput folder.
- Copy the JSON files to /mongo/import/ directory.
For each JSON file in the directory:
- Rename this JSON file to "data.json".
- Add a metadata entry with packet name / # in ```/mongo/labels.json```.
- Manually edit packet parameters to match above in ```/mongo/importfromjson.py```; then run it.
- Add both the txt file and JSON file to the ```/successfully imported``` directory.
- Rinse and repeat.
Finally, to generate metadata:
- Run ```python /mongo/aggregatestats.py```. Comment / uncomment out the appropriate code to run!

Notes:
- ```/mongo/metadata.py``` has the pure metadata (just aggregate output of mongo command). ```/mongo/metadata.py``` and ```/mongo/labels.py``` are merged to create the ```/mongo/output/metadata.py```.
- After done, copy the contents of the ```/mongo/output/``` directory to the ```/assets/packets``` folder in the Tycho app.


Formatting guidelines


TOSS-UP 1) MATH Short Answer
or
TOSS-UP 1. MATH Short Answer

Make sure you number the choices if a multi-choice question:
```
1. S is positive

2. S is negative

3. G is positive

4. G is negative

ANSWER: 2 and 3
```

If a multiple choice question, use W), X), Y), and Z) on newlines.

Make sure category is capitalized.

For square roots, use ```&radic;```
For powers such as x squared, use ```x<sup>2</sup>```
For subscripts such as Br<sub>2</sub>, use ```Br<sub>2</sub>```