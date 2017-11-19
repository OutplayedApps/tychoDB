 var fs = require("fs");
 console.log("\n *STARTING* \n");
// Get content from file
var contents = fs.readFileSync("nsbquestions.json");
// Define to JSON type
var jsonContent = JSON.parse(contents);
var output = []; // array of all questions
var outputSorted = {}; // array of all questions in object format (for write to file).
var metadata = {};
metadata.vendorNum = {};

for (var i = 0; i <= 1 ; i++) {
    var questions = jsonContent["MS"];
    var grade = "MS";
    if (i == 1) {
        questions = jsonContent["HS"];
        grade = "HS";
    }
    console.log(questions);

    for (var q in questions) {
        // q is 8_16_13, for example.
        var questionNum = q.split("_");
        questionNum = questionNum[questionNum.length - 1];

        var question = questions[q];
        question.grade = grade;
        //question.setNum = String(question.setNum);
        delete question.catDiff;
        question.vendorNum = "DOE-" + question.grade;
        question.questionNum = questionNum;
        output.push(question);

        var fileName = question.vendorNum + "-" + question.setNum + "-" + question.packetNum;
        
        if (!outputSorted[fileName]) outputSorted[fileName] = [];
        outputSorted[fileName].push(question);

        if (!metadata.vendorNum[question.vendorNum])
            metadata.vendorNum[question.vendorNum] = {};
        if (!metadata.vendorNum[question.vendorNum][question.setNum])
            metadata.vendorNum[question.vendorNum][question.setNum] = {};
        if (!metadata.vendorNum[question.vendorNum][question.setNum][question.packetNum])
            metadata.vendorNum[question.vendorNum][question.setNum][question.packetNum] = {"numQuestions": 0, "fileName": fileName};

        metadata.vendorNum[question.vendorNum][question.setNum][question.packetNum].numQuestions++;

    }
}

OUTPUT_DIR = "output/"

if (!fs.existsSync(OUTPUT_DIR)){
    fs.mkdirSync(OUTPUT_DIR);
}

fs.writeFile("output-pretty.json", JSON.stringify(output, null, 2), function(err) {
            if (err) {
                return console.log(err);
            }
            //res.write("Saved");
            console.log("Output pretty file was saved!");
});

fs.writeFile("output.json", JSON.stringify(output), function(err) {
            if (err) {
                return console.log(err);
            }
            //res.write("Saved");
            console.log("Output ugly file was saved!");
});

// full metadata
fs.writeFile(OUTPUT_DIR + "metadata.json", JSON.stringify(metadata, null, 2), function(err) {
            if (err) {
                return console.log(err);
            }
            console.log("Metadata was saved!");
});

// individual question files
for (let fileName in outputSorted) {
    fs.writeFile(OUTPUT_DIR + fileName + ".json", JSON.stringify(outputSorted[fileName], null, 2), function(err) {
                if (err) {
                    return console.log(err);
                }
                console.log("File " + fileName + ".json was saved!");
    });
}