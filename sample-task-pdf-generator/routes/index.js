'use strict';

const fs = require('fs');
const request = require('request');
const path = require('path');
const json2xls = require('json2xls');

module.exports = function (app) {
  // Index
  app.get('/pdf-panel', function (req, res) {
    res.render('index');
  });

  // Find all the questions from the provided JSON file
  app.post('/fetch-questions', function (req, res) {
    let jsonFile = req.body.jsonFile;

    console.log('JSON file: ', jsonFile);

    let answerKey = []

    fs.readFile(`./db/${jsonFile}.json`, (err, db) => {
      if (err) throw err;

      let questions = JSON.parse(db);

      console.log('Questions: ', questions.length);

      questions.forEach(qs => {
        let details = {
          'ID': '',
          'TYPE': '',
          'ANSWER_KEY': '',
          'PREV_YEAR': ''
        }

        // set the details
        details.ID = qs.id;
        details.TYPE = qs.type;
        details.PREV_YEAR = qs.previousYearPapers[0];
        
        // set the correct answer
        if (qs.type === "singleCorrect") {
          let rightAnswer;
          
          if (qs.options[0].isCorrect) {
            rightAnswer = 1;
          } else if (qs.options[1].isCorrect) {
            rightAnswer = 2;
          } else if (qs.options[2].isCorrect) {
            rightAnswer = 3;
          } else {
            rightAnswer = 4;
          }
          details.ANSWER_KEY = rightAnswer;
        } else if (qs.type === "numerical") {
          details.ANSWER_KEY = qs.correctValue
        } else if (qs.type === "multipleCorrect") {
          let rightAnswer = '';
          
          if (qs.options[0].isCorrect) rightAnswer = '1,';
          if (qs.options[1].isCorrect) rightAnswer += '2,';
          if (qs.options[2].isCorrect) rightAnswer += '3,';
          if (qs.options[3].isCorrect) rightAnswer += '4,';
          
          details.ANSWER_KEY = rightAnswer.slice(0, -1);
        } else {
          details.ANSWER_KEY = "ERROR"
        }

        answerKey.push(details)

      });

      // save xlsx
      let xls = json2xls(answerKey);
      fs.writeFileSync(`./for_qc_${jsonFile}.xlsx`, xls, 'binary');
      
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
