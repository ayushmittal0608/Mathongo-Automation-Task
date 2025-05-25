'use strict';

const fs = require('fs');
const request = require('request');

module.exports = function (app) {
  // Index
  app.get('/pdf-panel', function (req, res) {
    res.render('index');
  });

  // Find all the questions from the provided JSON file
  app.post('/fetch-questions', function (req, res) {
    let jsonFile = req.body.jsonFile;

    console.log('JSON file: ', jsonFile);

    fs.readFile(`./db/${jsonFile}.json`, (err, db) => {
      if (err) throw err;

      let questions = JSON.parse(db);

      console.log('Questions: ', questions.length);

      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify(questions));
    });
  });

  // Chapter-wise Question page
  app.get('/question', function (req, res) {
    res.render('question');
  });

  // Chapter-wise Question page
  app.get('/solution', function (req, res) {
    res.render('solution');
  });
};
