var express = require('express');
var app = express();
var path = require("path");
var bodyParser = require('body-parser')

app.use(express.static('static'));
app.use(bodyParser.json());

app.get('/', function(req,res){
  res.sendFile(path.join(__dirname+'/index.html'));
});

app.set('port', process.env.PORT || 8081);
app.listen(app.get('port'), function () {
  console.log('Server running at http://127.0.0.1:' + app.get('port') + '/');
});

