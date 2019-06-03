import os 
import boto3
import json
import csv


s3 = boto3.resource('s3')
bucket = s3.Bucket('tracking-metrics')
# Iterates through all the objects, doing the pagination for you. Each obj
# is an ObjectSummary, so it doesn't contain the body. You'll need to call
# get to get the whole body.
with open('unsubbed_tot.csv', 'w', newline = '') as csv_out:
    csv_writer = csv.writer(csv_out)

    unsubscribers = []
    clickers = []
    #files = ['2018/09/12', '2018/09/13', '2018/09/14', '2018/09/15', '2018/09/16', '2018/09/17']
    #files = ['2018/09/12', '2018/09/13', '2018/09/14', '2018/09/15', '2018/09/16', '2018/09/17', '2018/09/18', '2018/09/19', '2018/09/20', '2018/09/21', '2018/09/22', '2018/09/23', '2018/09/24']
    for obj in bucket.objects.filter(Prefix='2018'):
        key = obj.key
        body = obj.get()['Body'].read().decode('utf-8')
        print(key)
        for line in body.splitlines():
            json_data = json.loads(line)
            print(json_data['eventType'])
            print(json_data['mail']['destination'][0])
            
            if json_data['eventType'] == 'Click' and json_data['click']['link'] == 'http://email-unsub.s3-website-us-east-1.amazonaws.com':
                unsubscribers.append([json_data['mail']['destination'][0], json_data['mail']['timestamp']])
            #elif json_data['eventType'] == 'Click' and json_data['click']['link'] != 'http://email-unsub.s3-website-us-east-1.amazonaws.com':
                #clickers.append([json_data['mail']['destination'][0], json_data['click']['link']])
    
    #unsubs = list(set(unsubscribers))
    
    for email in unsubscribers:
        csv_writer.writerow([email[0], 'Unsubbed', email[1]])