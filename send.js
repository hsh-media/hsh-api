'use strict';
var https = require("https");
var http = require("http");
var AWS = require('aws-sdk');
var ses = new AWS.SES({
  region: 'us-east-1'
});

module.exports.main = (event, context, callback) => {
  const data = JSON.parse(event.body);

  const params = {
    Destination: {
      ToAddresses: [ "agrippa.sys@gmail.com" ],
    },
    Message: {
      Subject: {
        Data: data.title,
        Charset: 'UTF-8'
      },
      Body: {
        Text: {
          Data: data.context,
          Charset: "UTF-8"
        }
      }
    },
    Source: "auxili.sys@gmail.com"
  };

  ses.sendEmail(params, function(err) {
    callback(null, {
      statusCode: 200,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ status: "success" })
    });
  })
};
