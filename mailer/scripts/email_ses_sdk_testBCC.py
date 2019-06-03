import os
import csv
import boto3
import timeit
import urllib.request
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "Auxili <auxili.sys@gmail.com>"

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENTS = ['agrippa.sys@gmail.com', 'robconti16@gmail.com']

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the
# ConfigurationSetName=CONFIGURATION_SET argument below.
#CONFIGURATION_SET = "email_campaign"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-east-1"

# The subject line for the email.
SUBJECT = "April Newsletter"

# The full path to the file that will be attached to the email.
#ATTACHMENT = "path/to/customers-to-contact.xlsx"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = "Hello,\r\nPlease see the links attached to stay up to date."

# The HTML body of the email.
html_file = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<meta name="format-detection" content="telephone=no">
<meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=no;">
<meta http-equiv="X-UA-Compatible" content="IE=9; IE=8; IE=7; IE=EDGE" />

    <title>HSH Outreach</title>

    <style>

        @import url(http://fonts.googleapis.com/css?family=Roboto:300); /*Calling our web font*/

        /* Some resets and issue fixes */
        #outlook a { padding:0; }
        body{ width:100% !important; -webkit-text; size-adjust:100%; -ms-text-size-adjust:100%; margin:0; padding:0; }
        .ReadMsgBody { width: 100%; }
        .ExternalClass {width:100%;}
        .backgroundTable {margin:0 auto; padding:0; width:100%;!important;}
        table td {border-collapse: collapse;}
        .ExternalClass * {line-height: 115%;}
        /* End reset */

        .section1{
            width:20%;
            float:left;
            margin:0;
            padding:0;
        }

        .section2{
            width:60%;
            float:center;
            margin:0;
            padding:0;
        }

        .section3{
            width:20%;
            float:right;
            margin:0;
            padding:0;
        }


        @media screen and (max-width: 630px) {
            /* Display block allows us to stack elements */
            *[class="mobile-column"] {display: block;}

            /* Some more stacking elements */
            *[class="mob-column"] {float: none !important;width: 100% !important;}

            /* Hide stuff */
            *[class="hide"] {display:none !important;}

            /* This sets elements to 100% width and fixes the height issues too, a god send */
            *[class="100p"] {width:100% !important; height:auto !important;}

            /* For the 2x2 stack */
            *[class="condensed"] {padding-bottom:40px !important; display: block;}

            /* Centers content on mobile */
            *[class="center"] {text-align:center !important; width:100% !important; height:auto !important;}

            /* 100percent width section with 20px padding */
            *[class="100pad"] {width:100% !important; padding:20px;}

            /* 100percent width section with 20px padding left & right */
            *[class="100padleftright"] {width:100% !important; padding:0 20px 0 20px;}

            /* 100percent width section with 20px padding top & bottom */
            *[class="100padtopbottom"] {width:100% !important; padding:20px 0px 20px 0px;}

        }
    </style>


</head>

<body style="padding:0; margin:0">

<table align="center" width="640" cellspacing="0" cellpadding="0" bgcolor="#F2F3F4" class="100p">
    <tr>
        <td align="center" style="font-size:74px; color:#1C2833; line-height=0"><font face="Avenir, Arial, sans-serif"><span style="color:#1C2833; font-size:74px;"><b>HSH<b/></span><br />
            <span style="font-size:20px; color:#1C2833;"><b>Howard Stirk Holdings<b/></span></font>
        </td>
    </tr>
    <tr>
        <td height="25"></td>
    </tr>
</table>


<table align="center" width="640" cellspacing="0" cellpadding="0" class="100p">
    <tr>
        <td width="120" height="8" bgcolor="#F2F3F4"></td>
        <td width="400" height="8" bgcolor="#A569BD"></td>
        <td width="120" height="8" bgcolor="#F2F3F4"></td>
    </tr>
</table>


<table align="center" width="640" border="0" cellspacing="0" cellpadding="10" bgcolor="#F2F3F4" class="100p">
    <tr>
        <td align="center" style="font-size:40px; line-height:30px; color:#1C2833;"><font face="Bookman, Arial, sans-serif"><span style="color:#1C2833; font-size:40px; line-height:15px;"><b>April Newsletter<b/></span><br />
            <span style="font-size:18px; line-height:10px; color:#1C2833">Check out what HSH has been up to this month by clicking the image below.</span></font>
        </td>
    </tr>
    <tr>
        <td align="center">
            <a href="http://pub.lucidpress.com/1915518c-32c6-44a4-bbb4-910a5add235c/" target="_blank">
               <img src="https://i.ibb.co/crrssW3/Screenshot-79.png" border="0" alt="Show Thumbnail" width="440" height="640"/>
            </a>
        </td>
    </tr>
    <td height="1"></td>
</table>


<table align="center" width="640" cellspacing="0" cellpadding="0" class="100p">
    <tr>
        <td width="120" height="8" bgcolor="#F2F3F4"></td>
        <td width="400" height="8" bgcolor="#F4D03F"></td>
        <td width="120" height="8" bgcolor="#F2F3F4"></td>
    </tr>
</table>

<table align="center" width="640" cellspacing="0" cellpadding="15" bgcolor="#F2F3F4" class="100p">
    <tr>
        <td width="140" height="100" bgcolor="#F2F3F4"></td>
        <td width="360"><img src="https://image.ibb.co/dbRMEy/Strongcast_text_1.png" alt="Strongcast_text" width="360" height="100" border="0" style="display:block;"/></td>
        <td width="140" height="100" bgcolor="#F2F3F4"></td>
    </tr>
</table>


<table align="center" width="640" border="0" cellspacing="0" cellpadding="0" class="100p" bgcolor="#F2F3F4">
    <tr>
        <td height="10"></td>
    </tr>
    <tr>
        <td align="center" valign="top">
            <table border="0" cellpadding="0" cellspacing="0" class="100padtopbottom" width="600">
                <tr>
                    <td align="left" class="condensed" valign="top">
                        <table align="left" border="0" cellpadding="0" cellspacing="0" class="mob-column" width="290">
                            <tr>
                                <td valign="top" align="center">
                                    <table border="0" cellspacing="0" cellpadding="0">
                                        <tr>
                                            <td valign="top" align="center" class="100padleftright">
                                                <table border="0" cellspacing="0" cellpadding="0">
                                                    <tr>
                                                        <td width="90"></td>
                                                        <td width="200" align="center" style="font-size:18px; color:#1C2833;"><font face="Avenir, Arial, sans-serif">Join Armstrong Williams as he takes his 30 years of radio and television experience to the world of podcasting!</font></td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td height="10"></td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td width="20" class="hide"></td>
                    <td align="left" class="condensed" valign="top">
                        <table align="left" border="0" cellpadding="0" cellspacing="0" class="mob-column" width="290">
                            <tr>
                                <td valign="top" align="center">
                                    <table border="0" cellspacing="0" cellpadding="0">
                                        <tr>
                                            <td valign="top" align="center" class="100padleftright">
                                                <table border="0" cellspacing="0" cellpadding="0">
                                                    <tr>
                                                        <td width="290" align="center" style="font-size:18px; color:#1C2833;"><font face="Avenir, Arial, sans-serif"><b>Experience the Strongcast on these platforms:</b></font></td>
                                                    </tr>
                                                </table>
                                                <table align="center" border="0" cellspacing="0" cellpadding="0">
                                                    <tr>
                                                        <ul width="290" align="left" style="font-size:15px; color:#1C2833;"><font face="Avenir, Arial, sans-serif">
                                                            <li><a href="https://soundcloud.com/thestrongcast">Soundcloud</a></li>
                                                            <li><a href="https://itunes.apple.com/us/podcast/the-strongcast/id1299887231?mt=2">iTunes</a></li>
                                                            <li><a href="https://www.stitcher.com/podcast/armstrong-williams/the-strongcast?refid=stpr">Stitcher</a></li>
                                                            <li><a href="https://www.youtube.com/arightside">Youtube</a></li>
                                                            </font>
                                                        </ul>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>

<table align="center" width="640" cellspacing="0" cellpadding="0" class="100p">
    <tr>
        <td height="10" bgcolor="#F2F3F4"></td>
    </tr>
</table>

<table align="center" width="640" cellspacing="0" cellpadding="0" class="100p">
    <tr>
        <td width="120" height="8" bgcolor="#F2F3F4"></td>
        <td width="400" height="8" bgcolor="#CB4335"></td>
        <td width="120" height="8" bgcolor="#F2F3F4"></td>
    </tr>
</table>


<table align="center" width="640" border="0" cellspacing="0" cellpadding="20" bgcolor="#F2F3F4" class="100p">
    <tr>
        <td align="center" style="font-size:20px; color:#1C2833;"><font face="Avenir, Arial, sans-serif">Make sure to follow us on social media. New content is always being produced.</font></td>
    </tr>
</table>

<table align="center" width="640" border="0" cellspacing="0" cellpadding="20" class="100p" bgcolor="#F2F3F4">
    <tr>
        <td align="center" valign="top">
            <table border="0" cellpadding="0" cellspacing="0" class="100padtopbottom" width="600">
                <tr>
                    <td align="left" class="condensed" valign="top">
                        <table align="left" border="0" cellpadding="0" cellspacing="0" class="mob-column" width="290">
                            <tr>
                                <td valign="top" align="center">
                                    <table border="0" cellspacing="0" cellpadding="0">
                                        <tr>
                                            <td valign="top" align="center" class="100padleftright">
                                                <table border="0" cellspacing="0" cellpadding="0">
                                                    <tr>
                                                        <td width="135" align="center"><a href="https://www.facebook.com/RealArmstrongWilliams/?rc=p"><img src="https://image.ibb.co/juh9Wo/if_2018_social_media_popular_app_logo_facebook_3225194.png" alt="Facebook" width="70" height="70" border="0" style="display:block;"/></a></td>
                                                        <td width="20"></td>
                                                        <td width="135" align="center"><a href="https://www.youtube.com/channel/UCUeAJ8amaT9ZSI7NB5-yXcA"><img src="https://image.ibb.co/dOg3ro/if_2018_social_media_popular_app_logo_youtube_3225180.png" alt="Youtube" width="70" height="70" border="0" style="display:block;"/></a></td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td height="10"></td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td width="20" class="hide"></td>
                    <td align="left" class="condensed" valign="top">
                        <table align="left" border="0" cellpadding="0" cellspacing="0" class="mob-column" width="290">
                            <tr>
                                <td valign="top" align="center">
                                    <table border="0" cellspacing="0" cellpadding="0">
                                        <tr>
                                            <td valign="top" align="center" class="100padleftright">
                                                <table border="0" cellspacing="0" cellpadding="0">
                                                    <tr>
                                                        <td width="135" align="center"><a href="https://twitter.com/Arightside?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor"><img src="https://image.ibb.co/mKX9Wo/if_2018_social_media_popular_app_logo_twitter_3225183.png" alt="Twitter" width="70" height="70" border="0" style="display:block;"/></a></td>
                                                        <td width="20"></td>
                                                        <td width="135" align="center"><a href="https://www.instagram.com/arightside/?hl=en"><img src="https://image.ibb.co/bXMgcT/if_2018_social_media_popular_app_logo_instagram_3225191.png" alt="Instagram" width="70" height="70" border="0" style="display:block;"/></a></td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td height="10"></td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>


<table align="center" width="640" cellspacing="0" cellpadding="0" class="100p">
    <tr>
        <td width="120" height="8" bgcolor="#F2F3F4"></td>
        <td width="400" height="8" bgcolor="#E67E22"></td>
        <td width="120" height="8" bgcolor="#F2F3F4"></td>
    </tr>
</table>


<table align="center" width="640" border="0" cellspacing="0" cellpadding="8" bgcolor="#F2F3F4" class="100p">
    <tr>
        <td align="left" style="font-size:12px; color:gray;"><font face="Avenir, Arial, sans-serif">Howard Stirk Holdings LLC</font></td>
    </tr>
    <tr>
        <td align="left" style="font-size:12px; color:gray;"><font face="Avenir, Arial, sans-serif">You are receiving this email because you are on our list of subscribers. If you would like to be removed from this list click the unsubscribe link below.</font></td>
    </tr>
    <tr>
        <td align="left" style="font-size:12px; color:gray;"><font face="Avenir, Arial, sans-serif"><a href="http://email-unsub.s3-website-us-east-1.amazonaws.com"> Unsubscribe </a></font></td>
    </tr>
</table>

</body>
</html>

"""

#print(html_file)
#print(type(html_file))
# The character encoding for the email.
CHARSET = "utf-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name='us-east-1')

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
htmlpart = MIMEText(html_file.encode(CHARSET), 'html', CHARSET)

print(htmlpart)
print(type(htmlpart))
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

#with open('5-3_EL_1.csv', 'r') as csv_file:
#    csv_reader = csv.reader(csv_file)

#    cnt = 0
#    start_time= timeit.default_timer()
 #   for row in csv_reader:
 #       RECIPIENTS.append(row[0])
 #       cnt += 1

 #   print(RECIPIENTS)
  #  print(cnt)
  #  print(timeit.default_timer() - start_time)

cnt = 0
start_time = timeit.default_timer()

print(type(msg))

for to_address in RECIPIENTS:
    cnt += 1
    del msg['To']
    msg['To'] = to_address
    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[
                to_address
            ],
            RawMessage={
                'Data':msg.as_string(),
            },
            #ConfigurationSetName=CONFIGURATION_SET
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:")
        print(cnt),
        print(response['MessageId'])
        print(timeit.default_timer() - start_time)
print(timeit.default_timer() - start_time)
