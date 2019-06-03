import * as send_raw_email from "./libs/ses-lib";
import { success, failure } from "./libs/response-lib";


export async function main(event, context) {
  const data = JSON.parse(event.body);
  //console.log(data);
  const aws = require('aws-sdk');
  const AmazonS3URI = require('amazon-s3-uri');

  if (!data.title) {
      context.fail('Missing argument: subject');
  }

  if (!data.htmlfileURL && !data.context) {
      context.fail('Missing argument: html|text');
  }

  if (!data.mailfileURL && !data.testlist) {
    context.fail('Missing argument: email list');
  }

  var getList = {
    region: '',
    bucket: '', // your bucket name,
    key: '' // path to the object you're looking for
  };

  var getHTML = {
    region: '',
    bucket: '', // your bucket name,
    key: '' // path to the object you're looking for
  };
  var emaillist;
  var htmlbody;
  let url = data.htmlfileURL;
  var request = require('request').defaults({ encoding: 'utf-8' });
  request.get(url, function (err, resp, body) {
      htmlbody = body;
  });

  
  //console.log(request);
  //try {
  //  var uri = event.body.htmfilelURL;
  //  getHTML = AmazonS3URI(uri);
  //} catch(err) {
  //  console.warn(`${event.body} is not a valid S3 uri`); // should not happen because `uri` is valid in that example 
  //}

  //try {
  //  var uri = event.body.mailfilelURL;
  //  getList = AmazonS3URI(uri);
  //} catch(err) {
  //  console.warn(`${uri} is not a valid S3 uri`); // should not happen because `uri` is valid in that example 
  //}

  //const s3 = new aws.S3(); // Pass in opts to S3 if necessary

  //s3.getObject({ Bucket: getHTML.bucket, Key: getHTML.key }, function(err, data) {
      // Handle any error and exit
  //    if (err)
  //        return err;

  //  let htmlbody = data.Body.toString('utf-8'); // Use the encoding necessary
  //}); 

  //s3.getObject({ Bucket: getList.bucket, Key: getList.key }, function(err, data) {
  //  // Handle any error and exit
  //  if (err)
  //      return err;

  //  let emaillist = data.Body.toString('utf-8'); // Use the encoding necessary
  //}); 

  // var to      = event.email;
  var subject = data.title;
  var htmlBody;
  // var emaillist;
  var textBody = data.context;
  // var attachments = event.attachments;

  var testlist = data.testlist;
  var from    = "Auxili <auxili.sys@gmail.com>";
  var subject = data.title;
  var textBody = data.context;

  var ses_mail_bottom = "Subject: " + subject + "\n";
  ses_mail_bottom += "MIME-Version: 1.0\n";
  ses_mail_bottom += "Content-Type: multipart/alternative; boundary=\"NextPart\"\n\n";
  ses_mail_bottom += "--NextPart\n";
  ses_mail_bottom += "Content-Type: text/html; charset=utf-8\n\n";
  ses_mail_bottom += textBody;
  ses_mail_bottom += "--NextPart--";
  
  //var ses = new aws.SES({
  //  region: 'us-east-1'
 //});

  var list = testlist;
  if(emaillist){
    list = testlist + emaillist;
  } 
  //console.log(list);
  var addr = 'agrippa.sys@gmail.com';

  var ses_mail_bottom = "From: 'Auxili' <auxili.sys@gmail.com>\n";
  ses_mail_bottom += "To: " + addr + "\n";
  ses_mail_bottom = "Subject: " + subject + "\n";
  ses_mail_bottom += "MIME-Version: 1.0\n";
  ses_mail_bottom += "Content-Type: multipart/alternative; boundary=\"NextPart\"\n\n";
  ses_mail_bottom += "--NextPart\n";
  ses_mail_bottom += "Content-Type: text/html; charset=utf-8\n\n";
  ses_mail_bottom += textBody;
  ses_mail_bottom += "--NextPart--";

  var params = {
    RawMessage: { Data: ses_mail_bottom.toString(), },
    Destinations: [addr],
    Source: 'auxili.sys@gmail.com'
  };
  //console.log("About to send");
  //console.log(params);
  //await ses.sendRawEmail(params, function(err, data) {
  //  if(err) {
  //      console.log(err);
  //  } 
  //  else {
   //     console.log(data);
  //  }           
 // });
  try {
    var email = await ses.send_raw_email(params);
    email
      .then(data => {
        console.log("email submitted to SES", data);
      })
      .catch(error => {
        console.log(error);
      });
    console.log(email);
    return success(params);
  } catch (e) {
    return failure({ status: false });
  }
  //var email = ses.sendRawEmail(params).promise(); //function(err, data) {
    //console.log("callback...")
   // if(err){ 
   //   console.log(err);
    //} else {
   // console.log("===EMAIL SENT===");
   // console.log(data);
    
   // console.log("EMAIL CODE END");
   // console.log('EMAIL: ', email);
   // context.succeed(event);
  email
   .then(data => {
     console.log("email submitted to SES", data);
   })
   .catch(error => {
     console.log(error);
   });
  console.log(email);
}
