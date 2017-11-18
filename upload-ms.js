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
            str2 =  str2.replace(/([A-Za-z]*)  ([A-Za-z]*)/g, "$1 $2");
         str2 = str2.replace("MATH Math", "MATH");
            //console.log(str2);
            if (!~str2.indexOf(")") || str2.indexOf(")") > 10) {
                //if 3 TOSSUP ... etc. IF IT"S MISSING...
                str2 = str2.replace(/([0-9]{1,2})/, "$1)");
            }
            if (str2.match(/The toss-up and bonus for Question [0-9]{1,2}\) have been omitted./)) return;
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
            else if (~tossupQ.indexOf("Short Answer")) {
                category = tossupQ.substring(0, tossupQ.indexOf("Short Answer")).trim().toUpperCase();
            }
            else { //no category ...? defaults to SA instead.
                //tossupQ = tossupQ.replace(/([A-Z ]*)([A-Z])/g, "$1Short Answer $2");
                if (tossupQ.startsWith("MATH")) {
                    if (~tossupQ.indexOf("W)"))
                        tossupQ = "MATH Multiple Choice" + tossupQ.substring(4);
                    else
                        tossupQ = "MATH Short Answer" + tossupQ.substring(4);
                    
                }
                if (tossupQ.startsWith("GENERAL SCIENCE")) {
                    if (~tossupQ.indexOf("W)"))
                        tossupQ = "GENERAL SCIENCE Multiple Choice" + tossupQ.substring(4);
                    else
                        tossupQ = "GENERAL SCIENCE Short Answer" + tossupQ.substring(4);
                }
                if (tossupQ.startsWith("EARTH SCIENCE")) {
                    if (~tossupQ.indexOf("W)"))
                        tossupQ = "EARTH SCIENCE Multiple Choice" + tossupQ.substring(4);
                    else
                        tossupQ = "EARTH SCIENCE Short Answer" + tossupQ.substring(4);
                }
                category = tossupQ.substring(0, tossupQ.indexOf(~tossupQ.indexOf("W)") ? "Multiple Choice" : "Short Answer")).trim().toUpperCase();
                
            }
            category = category.trim();
            var categoryList = {
              "EARTH SCIENCE": 0,
              "EARTH AND SPACE": 0,
              "EARTH AND SPACE SCIENCE": 0,
              "ASTRONOMY": 0,
              "LIFE SCIENCE": 1,
              "PHYSICAL SCIENCE": 3,
              "MATHEMATICS":4,
              "MATH":4,
              "ENERGY":5,
              "GENERAL SCIENCE": 6
            };
            var catName = category+"";
            category = categoryList[category];
            
            var tossupA = strBetween(str2, "ANSWER: ", "BONUS");
            str2 = str2.substring(str2.indexOf("BONUS"));

            var bonusQ = strBetween(str2, ") ", "ANSWER:");
            var bonusA = strBetween(str2, "ANSWER: ");

             if (tossupQ && tossupA && bonusQ && bonusA && typeof category == 'undefined') throw "ERRORIS" + catName+"."+category+"\n"+tossupQ+"\nSTR2 IS"+str2+"\nROUNDSTUFFIS"+setNum+"."+roundNum;
           
            
            if (tossupQ) //if not empty string.
            {
                data.questionsMS[setNum+"_"+roundNum+"_"+questionNum] = {
                "tossupQ": tossupQ,
                "tossupA": tossupA,
                "bonusQ": bonusQ,
                "bonusA": bonusA,
                "category": category,
                "setNum": setNum,
                "roundNum": roundNum,
                "catDiff": category+"."+roundNum
                };
        
            console.log(setNum+"/"+roundNum+"."+JSON.stringify(data.questionsMS[setNum+"_"+roundNum+"_"+questionNum]).substring(0, 50));
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
    if (setNum == 1) {
        roundString = "m_round";
        if (roundNum < 10)
            roundString += "0"
    }
    if (setNum == 2) roundString = "Sample_Questions_r";
    if (setNum == 3) roundString = "Round-";
    if (setNum == 7) roundString = "MS_Round-";

    var afterString = "";
    if (setNum == 3) afterString = "C-MS";

    if (setNum == 8) {
        roundString = "Round-";
        afterString = "-A";
    }

var path = "http://science.energy.gov/~/media/wdts/nsb/pdf/MS-Sample-Questions/Sample-Set-"+setNum+"/"+roundString+roundNum+afterString+".pdf"; 
console.log(path);
//request.get(path, function (error, response, body) {
    process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
    request({url: path, encoding: null}, function (error, response, body) {

//http.get(url.parse(path), function(response) {
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
        str.replace(/\n\n/g, "\n");
        while (~str.indexOf("TOSS-UP"))
        {
            /*if (str.indexOf("TOSS-UP")>10 && ~str.indexOf) {
                console.log("===SOMETHING WEIRD===", str);
                str = str.slice(str.indexOf(")")+1); //removes the number 3) from it and adds tossup.
                str = "100) TOSS-UP" + str;
                console.log("===END SOMETHING WEIRD===", str);
            }*/
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
        console.log("Progress: "+progress+" of "+totalProg+"."+"Setnum: "+setNum+"Roundnum: "+roundNum);
        callback();
    });


        pdfParser.parseBuffer(body);

});
    

}

//getText(1, 8, function() {console.log(data);});

var array = [];
var data = {};
data.questionsMS = {};

//console.log(JSON.stringify(data));
        for (var setNum = 8; setNum <=8; setNum++) {
            for (var roundNum = 1; roundNum <= 18; roundNum++) {
              if (roundNum > 10 && (setNum == 2)) continue;
              if (roundNum > 15 && (setNum == 3)) continue;
              if (roundNum > 17 && (setNum == 4)) continue;
              if (roundNum > 16 && (setNum == 5)) continue;
              if (roundNum > 17 && (setNum == 6)) continue;
              if (roundNum > 15 && (setNum == 7)) continue;
                if (roundNum > 17 && (setNum == 8)) continue;
              
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
            fs.writeFile("output-ms-8.json", JSON.stringify(data), function(err) {
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
