import os 
import boto3
import json
import csv


s3 = boto3.resource('s3')
bucket = s3.Bucket('tracking-metrics')
# Iterates through all the objects, doing the pagination for you. Each obj
# is an ObjectSummary, so it doesn't contain the body. You'll need to call
# get to get the whole body.
with open('florence_sept_links.csv', 'w', newline = '') as csv_out:
    csv_writer = csv.writer(csv_out)

    #files = ['2018/08/14', '2018/08/15', '2018/08/16', '2018/08/17', '2018/08/18', '2018/08/19', '2018/08/20', '2018/08/21', '2018/08/22', '2018/08/23', '2018/08/24', '2018/08/25', '2018/08/26', '2018/08/27', '2018/08/28', '2018/08/29', '2018/08/30', '2018/08/31', '2018/09/01', '2018/09/02', '2018/09/03', '2018/09/04', '2018/09/05', '2018/09/06', '2018/09/07', '2018/09/08', '2018/09/09', '2018/09/10', '2018/09/11']
    #files = ['2018/09/12', '2018/09/13', '2018/09/14', '2018/09/15', '2018/09/16', '2018/09/17']
    files = ['2018/09/23', '2018/09/24', '2018/09/25', '2018/09/26', '2018/09/27', '2018/09/28', '2018/09/29', '2018/09/30', '2018/10/01', '2018/10/02', '2018/10/03', '2018/10/04', '2018/10/05', '2018/10/06', '2018/10/07', '2018/10/08', '2018/10/09', '2018/10/10']
    for f in files:
        for obj in bucket.objects.filter(Prefix=f):
            key = obj.key
            body = obj.get()['Body'].read().decode('utf-8')
            print(key)
            for line in body.splitlines():
                json_data = json.loads(line)
                print(json_data['eventType'])
                print(json_data['mail']['destination'][0])
                
                if json_data['eventType'] == 'Click' and json_data['click']['link'] != 'http://email-unsub.s3-website-us-east-1.amazonaws.com':
                    csv_writer.writerow([json_data['mail']['destination'][0], 'Clicked', json_data['click']['link']])