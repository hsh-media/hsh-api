import os
import csv
import json
import boto3
import timeit
import urllib.request
from urllib.parse import urlparse, quote
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def main(event, context):

    # event.body.htmlfileURL: html url
    # event.bodyaddr csv url OR test emails list
    # Sender email addr
    # title
    # content
    #print(event['body'][0])

    data = json.loads(event['body'])


    #data2 = json.loads(data)
    #print(data)
    #url11 = urllib.parse.quote(data['htmlfileURL'])
    #print(data['htmlfileURL'])
    #print(url11)
    htmlfile = urllib.request.urlopen(data['htmlfileURL']).read().decode('utf-8')
    #print(type(htmlfile))

    #print(htmlfile)
    mailfile = None
    if not data['mailfileURL']:
        mailfile = None 
    else:
        mailfile = urlparse(data['mailfileURL'])
    # As this will always have a leading slash it's safe to strip
    # print(o.path[1:])

    # Or often what you need is the s3 bucket and key separately.
    #htmlbucket, htmlkey = html.path.split('/', 2)[1:]
   
    # print(bucket)
    # print(key)

    # Connect to s3
    #s3 = boto3.client('s3')
    
    #s3_htmlfile = s3.get_object(Bucket=htmlbucket, Key=htmlkey)
    #htmlfile = s3_htmlfile['Body'].read()

    #mailfile = None 
    #if not data['mailfileURL']:
    #    mailbucket, mailkey = mail.path.split('/', 2)[1:]
    #    s3_mailfile = s3.get_object(Bucket=mailbucket, Key=mailkey)
    #    mailfile_csv = s3_mailfile['Body'].read().splitline(True)
    #    mailfile = csv.reader(mailfile_csv)

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "HSH <auxili.sys@gmail.com>"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENTS = []
    for emails in data['testlist']:
        RECIPIENTS.append(emails['email'])

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = data['content']

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.

    # CONFIGURATION_SET = "email_campaign"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = data['title']

    # The character encoding for the email.
    CHARSET = "utf-8"

    # Create a new SES resource and specify a region.
    ses = boto3.client('ses',region_name=AWS_REGION)

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    #msg['BCC'] = 'rconti@umd.edu'

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(htmlfile.encode(CHARSET), 'html', CHARSET)

    print(type(htmlpart))
    print(htmlpart)
    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    # Define the attachment part and encode it using MIMEApplication.
    #att = MIMEApplication(open(ATTACHMENT, 'rb').read())

    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    #att.add_header('Content-Disposition','attachment',filename=os.path.basename(ATTACHMENT))

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    # Add the attachment to the parent container.
    #msg.attach(att)
    #print(msg)
    if mailfile is not None:
        cnt = 0
        for row in mailfile:
            RECIPIENTS.append(row[0])
            cnt += 1

    print(type(msg))
    cnt = 0
    for to_address in RECIPIENTS:
        cnt += 1
        del msg['To']
        msg['To'] = to_address
        try:
            #Provide the contents of the email.
            response = ses.send_raw_email(
                Source=SENDER,
                Destinations=[
                    to_address
                ],
                RawMessage={
                    'Data':msg.as_string(),
                },
                # ConfigurationSetName=CONFIGURATION_SET
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:")
            print(cnt),
            print(response['MessageId'])
