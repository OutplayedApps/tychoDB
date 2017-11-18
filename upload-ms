//var pdfUtil = require('pdf-to-text');
var fs = require('fs');
var request = require('request');
//var PDFJS =require('../../build/dist');
var PDFParser = require('pdf2json');
 
 var http = require('http');
 var url = require('url');
 var fs = require('fs');
 var async = require('async');
 var Sync = require('sync');
var deasync = require('deasync');
var progress = 0;
var totalProg = 0;
     function processAndAdd(str2, setNum, roundNum, questionNum) {
            var pageEndStr = "\n----------------Page";
            var pageEndIndex = str2.indexOf(pageEndStr);
            if (~pageEndIndex) {
                str2 = str2.substring(0, pageEndIndex);
            }
            //console.log(str2);
            var tossupQ = strBetween(str2, ") ", "ANSWER:");
            var category, type;
            if (~tossupQ.indexOf("Multiple Choice")) {
                category = tossupQ.substring(0, tossupQ.indexOf("Multiple Choice")).trim().toUpperCase();
            }
            else if (~tossupQ.indexOf("Multiple choice")) {
                category = tossupQ.substring(0, tossupQ.indexOf("Multiple choice")).trim().toUpperCase();
            }
            else if (~tossupQ.indexOf("Short answer")) {
                category = tossupQ.substring(0, tossupQ.indexOf("Short answer")).trim().toUpperCase();
            }
            else {
                category = tossupQ.substring(0, tossupQ.indexOf("Short Answer")).trim().toUpperCase();
            }
            category = category.trim();
            var categoryList = {
              "EARTH SCIENCE": 0,
              "EARTH AND SPACE": 0,
              "ASTRONOMY": 0,
              "BIOLOGY": 1,
              "CHEMISTRY": 2,
              "PHYSICS": 3,
              "MATHEMATICS":4,
              "MATH":4,
              "ENERGY":5,
              "GENERAL SCIENCE": 6,
              "COMPUTER SCIENCE": 7
            };
            var catName = category+"";
            category = categoryList[category];
            
            var tossupA = strBetween(str2, "ANSWER: ", "BONUS");
            str2 = str2.substring(str2.indexOf("BONUS"));

            var bonusQ = strBetween(str2, ") ", "ANSWER:");
            var bonusA = strBetween(str2, "ANSWER: ");

             if (tossupQ && tossupA && bonusQ && bonusA && typeof category == 'undefined') throw "ERRORIS" + catName+"."+category+"\n"+tossupQ;
           
            
            if (tossupQ) //if not empty string.
            {
                data.questions[setNum+"_"+roundNum+"_"+questionNum] = {
                "tossupQ": tossupQ,
                "tossupA": tossupA,
                "bonusQ": bonusQ,
                "bonusA": bonusA,
                "category": category,
                "setNum": setNum,
                "roundNum": roundNum,
                "catDiff": category+"."+roundNum
                };
        
            console.log(JSON.stringify(data.questions[setNum+"_"+roundNum+"_"+questionNum]).substring(0, 100));
            }
    }

    function strBetween(input, s1, s2) {
        if (s2)
            return input.substring(input.indexOf(s1) + s1.length, input.indexOf(s2)).replace(/___*/g, "").trim();
        else
            return input.substring(input.indexOf(s1) + s1.length).replace(/___*/g, "").trim();
    }

var getText = function(setNum, roundNum, callback) {

    var roundString = "round";
    if (setNum == 6) roundString = "Sample6_ROUND";
    if (setNum == 7 || setNum == 3) roundString = "ROUND-";

    var afterString = "";
    if (setNum == 3) afterString = "C";
var path = "http://science.energy.gov/~/media/wdts/nsb/pdf/HS-Sample-Questions/Sample-Set-"+setNum+"/"+roundString+roundNum+afterString+".pdf"; 
console.log(path);
//request.get(path, function (error, response, body) {
    
http.get(url.parse(path), function(response) {
    //if (!error && response.statusCode == 200) {
        //var csv = body;
        //res.send("hi");
        //res.send(body);
        var pdfParser = new PDFParser(this, 1);
        
           pdfParser.on("pdfParser_dataError", function (errData) {
                console.log("errored"+JSON.stringify(errData));
            console.log(setNum+"."+roundNum);
            //callback();
            //throw JSON.stringify(errData);
            getText(setNum, roundNum, callback);
           //return JSON.stringify(errData);  //res.end();
           
           });
    pdfParser.on("pdfParser_dataReady", function (pdfData) {
        //console.log("done" + pdfParser.getRawTextContent());
        console.log("done");
        var txt = pdfParser.getRawTextContent(); //res.end();
        //console.log(txt);
        var str = txt;
        var questionNum = 1;
        while (~str.indexOf("TOSS-UP"))
        {
            str = str.substring(str.indexOf("TOSS-UP")+7);
            var str22 = str.substring(0, str.indexOf("TOSS-UP"));
            processAndAdd(str22, setNum, roundNum, questionNum);
            questionNum++;
            //console.log(str2+"HUHU");
        }
        questionNum++;
        str22 = str;
        processAndAdd(str22, setNum, roundNum, questionNum);
                progress++;
        console.log("Progress: "+progress+" of "+totalProg);
        callback();
    });
var data = [];
   response.on('data', function(chunk) {
        data.push(chunk);
    }).on('end', function() {
        //at this point data is an array of Buffers
        //so Buffer.concat() can make us a new Buffer
        //of all of them together
        var buffer = Buffer.concat(data);
        //console.log(buffer.toString('base64'));

        pdfParser.parseBuffer(buffer);
    });
});
    

}

//getText(1, 8, function() {console.log(data);});

var array = [];
var data = {};
data.questions = {};

//console.log(JSON.stringify(data));
        for (var setNum = 1; setNum <=7; setNum++) {
            for (var roundNum = 1; roundNum <= 17; roundNum++) {
              if (roundNum > 15 && (setNum == 5 || setNum ==6)) continue;
                array.push({"setNum":setNum,"roundNum":roundNum});
                totalProg++;
            }
        }

        console.log(array);

function main() {

       //async.each(array, function(item, callback) {
           for (var i in array) {
               var item = array[i];
                getText(item.setNum, item.roundNum, function() {});

            deasync.sleep(10);
           }
           //getText(1,4,callback);
           //deasync.sleep(2000);
       //},
       while (progress < totalProg)
        deasync.sleep(100);

        console.log(JSON.stringify(data));
       done();
        function done() {
            console.log("finished");
            fs.writeFile("output.json", JSON.stringify(data), function(err) {
                                    if(err) {
                                        return console.log(err);
                                    }
                                    //res.write("Saved");
                                    console.log("The file was saved!");
                                }); 
        };
        //console.log(array);

}
main();
