import aws from "aws-sdk";

export function send_raw_email(params) {
    const ses = new aws.SES({
        region: 'us-east-1'
    });

    return ses.sendRawEmail(params).promise();
}