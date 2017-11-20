//var pdfUtil = require('pdf-to-text');
var fs = require('fs');
var request = require('request');
//var PDFJS =require('../../build/dist');
var PDFParser = require('pdf2json');
var mammoth = require('mammoth');
var http = require('http');
var url = require('url');
var fs = require('fs');
var progress = 0;
var totalProg = 0;

function processAndAdd(str2, setNum, roundNum, questionNum) {
    var pageEndStr = "\n----------------Page";
    var pageEndIndex = str2.indexOf(pageEndStr);
    if (~pageEndIndex) {
        str2 = str2.substring(0, pageEndIndex);
    }
    str2 = str2.replace("EARTH ANDE SPACE", "EARTH AND SPACE");
    //console.log(str2);
    var tossupQ = strBetween(str2, ") ", "ANSWER:");
    if (tossupQ.match("\d*\.")) {
        tossupQ = strBetween(str2, ". ", "ANSWER:");
    }
    
    var category = "OTHER";
    var possibleStarts = ["Multiple Choice", "Multiple choice", "Short answer", "Short Answer", "SHORT ANSWER", "MULTIPLE CHOICE"];
    for (var i in possibleStarts) {
        var possibleStart = possibleStarts[i];
        if (~tossupQ.indexOf(possibleStart)) {
            category = tossupQ.substring(0, tossupQ.indexOf(possibleStart)).trim().toUpperCase();
            break;
        }
    }
    category = category.trim();
    var categoryList = {
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
    var catName = category + "";
    category = categoryList[category];
    var tossupA = strBetween(str2, "ANSWER: ", "BONUS");
    str2 = str2.substring(str2.indexOf("BONUS"));
    var bonusQ = strBetween(str2, ") ", "ANSWER:");
    var bonusA = strBetween(str2, "ANSWER: ");
    if (tossupQ && tossupA && bonusQ && bonusA && typeof category == 'undefined')
            throw "ERRORIS" + setNum + ", #" + roundNum + ":" + catName + "." + category + "\n" + tossupQ;
    var data = {};
    if (tossupQ) //if not empty string.
    {
        //data.questions[setNum + "_" + roundNum + "_" + questionNum] = {
        var data = {
            "tossupQ": tossupQ,
            "tossupA": tossupA,
            "bonusQ": bonusQ,
            "bonusA": bonusA,
            "category": category,
            "setNum": setNum,
            "roundNum": roundNum,
            "vendorNum": "vendor",
            "questionNum": questionNum
        };
        //console.log(data);
        //};
        //console.log(JSON.stringify(data.questions[setNum + "_" + roundNum + "_" + questionNum]).substring(0, 10));
    }
    return data;
}

function strBetween(input, s1, s2) {
    if (s2) return input.substring(input.indexOf(s1) + s1.length, input.indexOf(s2)).replace(/___*/g, "").trim();
    else return input.substring(input.indexOf(s1) + s1.length).replace(/___*/g, "").trim();
}
var getText = function(setNum, roundNum, callback) {
    var roundString = "round";
    if (setNum == 6) roundString = "Sample6_ROUND";
    if (setNum == 7 || setNum == 3) roundString = "ROUND-";
    if (setNum == 8) roundString = "Round-";
    var afterString = "";
    if (setNum == 3) afterString = "C";
    if (setNum == 8) afterString = "-A";
    var path = "http://science.energy.gov/~/media/wdts/nsb/pdf/HS-Sample-Questions/Sample-Set-" + setNum + "/" + roundString + roundNum + afterString + ".pdf";
    console.log(path);
    process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
    request({
        url: path,
        encoding: null
    }, function(error, response, body) {
        parsePDFBuffer(body, setNum, roundNum, callback);
    });
}

/* Actual pdf parsing work and adding to file json.
 */
function parsePDFBuffer(path, setNum=1, roundNum=1, callback) {
    var pdfParser = new PDFParser();
        pdfParser.on("pdfParser_dataError", function(errData) {
            console.log("errored" + JSON.stringify(errData));
            console.log(setNum + "." + roundNum);
            //callback();
            //throw JSON.stringify(errData);
            //getText(setNum, roundNum, callback);
            //return JSON.stringify(errData);  //res.end();
        });
        pdfParser.on("pdfParser_dataReady", function(pdfData) {
            //console.log("done" + pdfParser.getRawTextContent());
            console.log("data ready for this pdf: ");
            var txt = pdfParser.getRawTextContent(); //res.end();
            console.log(txt);
            writeData(setNum, roundNum , data, callback);

        });
        // console.log(body);
        //pdfParser.parseBuffer(body);
        pdfParser.loadPDF(path);
}

// parses and writes data to file.
function writeData(setNum, roundNum, txt, callback) {
    var fullData = [];
            var str = txt;
            var questionNum = 1;
            while (~str.indexOf("TOSS-UP")) {
                str = str.substring(str.indexOf("TOSS-UP") + 7);
                var str22 = str.substring(0, str.indexOf("TOSS-UP"));

                fullData.push(processAndAdd(str22, setNum, roundNum, questionNum));
                questionNum++;
                //console.log(str2+"HUHU");
            }
            questionNum++;
            str22 = str;
            fullData.push(processAndAdd(str22, setNum, roundNum, questionNum));
            progress++;
            console.log("Progress: " + progress + " of " + totalProg);
            if (callback) callback();
            return fullData;
}


function main() {
    /*for (var i in array) {
        var item = array[i];
         getText(item.setNum, item.roundNum, function() {});

     deasync.sleep(10);
    }*/
    // Read the 
    var dirname = "docx files input";
     fs.readdir(dirname, function (err, list) {
       // Return the error if something went wrong
       if (err)
         console.log("ERROR! " + err);

       // For every file in the list
       var promises = [];
       var fileData = [];
       list.forEach(function (filename) {
         // Full path of that file
         // path = dir + "/" + file;
            var path = dirname + "/" +  filename;
            console.log(path);
            var setNum = 0;
            var roundNum = 0;
            mammoth.extractRawText({path: path}).then((data) => {
                //console.log(data.value.substring(10));
                fs.writeFile("./txt/" + filename + ".txt", data.value, function(err) {
                    if (err) {
                        return console.log(err);
                    }
                    //res.write("Saved");
                console.log("The file was saved!");
                });
            }).catch(function(e) {
                console.log(e);
            })
            // parsePDFBuffer(dirname + "/" +  filename);
       });

        /*Promise.all(promises).then(() => {
            var fullData = [];
            for (var i in fileData) {
                var data = fileData[i];
                writeToFile(data.fileName, writeData(data.setNum, data.roundNum, data.data));
            }
            
        }
        );*/
     });


function writeToFile(fileName, data) {
        console.log("finished");
        fs.writeFile("./" + fileName + ".json", JSON.stringify(data, null, 2), function(err) {
            if (err) {
                return console.log(err);
            }
            //res.write("Saved");
            console.log("The file was saved!");
        });
    };
}
main();