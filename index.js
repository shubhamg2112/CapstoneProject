var express = require('express');
var mongoose = require('mongoose');
var bodyparser = require('body-parser');
var cors = require('cors');
var path = require('path');

var app = express();

const port  = 3000;

app.listen(port, ()=> {
console.log("The server is started on port" + port + ".")
});