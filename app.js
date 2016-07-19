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
    res.writeHead(200, {"Content-Type": "application/json"});
    res.end(JSON.stringify(jobConfig));
});

app.post('/invoke', function (req, res) {
    console.log('Invoked new job conversion.');
    var postMessage = req.body;
    var inputExtension = postMessage.input.type;
    var outputExtension = postMessage.output.type;
    var message = '';
    
    var configKey = inputExtension + "_to_" + outputExtension;
    var settings = jobConfig[configKey];
    if(typeof(settings) != 'undefined')
    {
        // todo: check for empty component base directory.
        var command = __dirname + "\\pipeline\\" + getComponentBaseDir(settings.command) + settings.command;
        
        var errMessage = "";
        var outputMessage = "";
        
        var exec = require('child_process').exec(command, function(err, stdout, stderr){
            if(err){
                errMessage = err;
                console.error(err);
                return;
            }
            console.log(stdout);
        });
        
        res.writeHead(200, {"Content-Type": "application/json"});
        res.end(JSON.stringify({'status':'ok','message' : 'Executed following command - ' + settings.command}));        
    }
    else
    {
        res.writeHead(400, {"Content-Type": "application/json"});
        res.end(JSON.stringify({'status':'error','message' : 'Missing config key for - ' + configKey}));
    }
})

function getComponentBaseDir(command){
		if(command.startsWith("dp2")){
			return "dp2\\";
		}
		else if(command.startsWith("pipeline")){
			return "dp1\\";
		}
		else if(command.startsWith("extras")){
			return "extras\\";
		}
		else if(command.startsWith("daisy")){
			return "word\\";
		}
		else{
			console.log("Invalid Command : " + command);
            return "";
        }
}

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

function initializeConfig(){
    var xml2js = require('xml2js');
    var parser = new xml2js.Parser();
    
    fs.readFile(__dirname + CONVERTER_LIST, function(err, data) {
        parser.parseString(data, function (err, result) {
            jobConfig = buildConfigJSON(result);
        });
    });
}

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

var server = app.listen(process.env.PORT || 3000, function () {
  var host = server.address().address
  var port = server.address().port
  
  initializeConfig();
  
  console.log("API end point listening at http://%s:%s", host, port);
})