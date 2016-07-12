var express = require('express');
var app = express();
var fs = require("fs");

app.get('/ping', function (req, res) {
    console.log('Ping received.');
    getJavaVersion(res);
})

function getJavaVersion(res){
    var spawn = require('child_process').spawn('java',['-version']);
    spawn.on('error', function(err){
        res.end('Unable to find Java installation or encountered other error.' + err);
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

var server = app.listen(8081, function () {
  var host = server.address().address
  var port = server.address().port

  console.log("API end point listening at http://%s:%s", host, port);
})