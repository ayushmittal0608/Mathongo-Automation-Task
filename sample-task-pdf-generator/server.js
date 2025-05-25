'use strict';
const express = require('express');
const routes = require('./routes/index.js');

const port = process.env.PORT || 3002;

const app = express();

app.use(express.json());
app.use(express.urlencoded({
  extended: true
}));

app.use(express.static(__dirname + '/public'));
app.set('view engine', 'ejs');

routes(app);

app.listen(port, function () {
  console.log(`Server running. Open the url http://localhost:${port}/pdf-panel in your browser`);
});