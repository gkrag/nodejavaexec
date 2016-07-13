var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var fs = require("fs");
var AZURE_JDK_PATH = 'D:\\Program Files\\Java\\jdk1.8.0_25\\bin';
var CONVERTER_LIST = "\\pipeline\\_scr_desc_";
var jobConfig = null;

// initialize JDK path
process.env.PATH += ';' + AZURE_JDK_PATH + ';';

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));

app.get('/ping', function (req, res) {
    console.log('Ping received.');
    getJavaVersion(res);
})

app.get('/config', function(req, res){
    var xml2js = require('xml2js');
    var parser = new xml2js.Parser();
    
    fs.readFile(__dirname + CONVERTER_LIST, function(err, data) {
        parser.parseString(data, function (err, result) {
            jobConfig = buildConfigJSON(result);
            res.writeHead(200, {"Content-Type": "application/json"});
            res.end(JSON.stringify(jobConfig));
        });
    });
});

function buildConfigJSON(config){
    var configJSON = {};
    
    if(config){
        for(var i = 0; i < config.scripts.script.length; i++){
            var configNode = config.scripts.script[i];
            var type = configNode.$.type;
            configJSON[configNode.$.name] = {}
            configJSON[configNode.$.name]['type'] = type;
            if(type = 'simple')
            {
                if(typeof(configNode.input) != 'undefined' && typeof(configNode.ext) != 'undefined')
                    configJSON[configNode.$.name]['input'] = {'type' : configNode.input[0], 'extension' : configNode.ext[0]};
                    
                if(typeof(configNode.command) != 'undefined')
                    configJSON[configNode.$.name]['command'] = configNode.command[0];
                    
                if(typeof(configNode.output) != 'undefined' && typeof(configNode.type) != 'undefined' && typeof(configNode.extension) != 'undefined')
                    configJSON[configNode.$.name]['output'] = {'type' : configNode.output[0], 'filetype': configNode.type[0], 'extension': configNode.extension[0]}; 
            }
            else if(type = 'complex')
            {
                
            }
        }
    }
    return configJSON;
}

app.post('/invoke', function (req, res) {
    console.log('Invoked new job conversion.');
    var postMessage = req.body;
    
    
    
    
    
    res.writeHead(200, {"Content-Type": "application/json"});
    res.end(JSON.stringify({'status':'ok'}));
})

function getJavaVersion(res){
    var spawn = require('child_process').spawn('java',['-version']);
    spawn.on('error', function(err){
        res.end('Unable to find Java installation or encountered other error.' + process.env.PATH + err);
    })
    spawn.stderr.on('data',function(data){
       data = data.toString().split('\n')[0];
       var javaVersion = new RegExp('java version').test(data) ? data.split(' ')[2].replace(/"/g, '') : false;
        if (javaVersion != false) {
            res.end('Following Java version is installed - ' + javaVersion);
        } else {
            res.end('No Java VM installed.');
        }
    });
}


var server = app.listen(process.env.PORT || 3000, function () {
  var host = server.address().address
  var port = server.address().port

  console.log("API end point listening at http://%s:%s", host, port);
})