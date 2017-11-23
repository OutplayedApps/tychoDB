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


function main() {
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