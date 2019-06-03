import os 
import boto3
import json
import csv


s3 = boto3.resource('s3')
bucket = s3.Bucket('compliance-metrics')
# Iterates through all the objects, doing the pagination for you. Each obj
# is an ObjectSummary, so it doesn't contain the body. You'll need to call
# get to get the whole body.
with open('sent_august.csv', 'w', newline = '') as csv_out:
    csv_writer = csv.writer(csv_out)

    cnt = 0
    cnt_b = 0
    cnt_c = 0
    bounce = []
    complaint = []
    sent = []
    #files = ['2018/08/14', '2018/08/15', '2018/08/16', '2018/08/17', '2018/08/18', '2018/08/19', '2018/08/20', '2018/08/21', '2018/08/22', '2018/08/23', '2018/08/24', '2018/08/25', '2018/08/26', '2018/08/27', '2018/08/28', '2018/08/29', '2018/08/30', '2018/08/31', '2018/09/01', '2018/09/02', '2018/09/03', '2018/09/04', '2018/09/05', '2018/09/06', '2018/09/07', '2018/09/08', '2018/09/09', '2018/09/10', '2018/09/11']
    #files = ['2018/09/12', '2018/09/13', '2018/09/14', '2018/09/15', '2018/09/16', '2018/09/17', '2018/09/18', '2018/09/19', '2018/09/20', '2018/09/21', '2018/09/22', '2018/09/23', '2018/09/24']
    #files = ['2018/09/24', '2018/09/25', '2018/09/26', '2018/09/27', '2018/09/28', '2018/09/29', '2018/09/30', '2018/10/1', '2018/10/2', '2018/10/3']
    #files = ['2018/09/24', '2018/09/25', '2018/09/26', '2018/09/27', '2018/09/28', '2018/09/29', '2018/09/30', '2018/10/1', '2018/10/2', '2018/10/3', '2018/10/4', '2018/10/5', '2018/10/6', '2018/10/7', '2018/10/8', '2018/10/9', '2018/10/10', '2018/10/11', '2018/10/12', '2018/10/13', '2018/10/14', '2018/10/15', '2018/10/16', '2018/10/17', '2018/10/18', '2018/10/19', '2018/10/20', '2018/10/21', '2018/10/22', '2018/10/23', '2018/10/24', '2018/10/25', '2018/10/26']
    #files = ['2018/10/26', '2018/10/27', '2018/10/28', '2018/10/29', '2018/10/30', '2018/10/31', '2018/11/1']
    files = ['2018/08','2018/09', '2018/10', '2018/11']
    for f in files:
        for obj in bucket.objects.filter(Prefix=f):
            key = obj.key
            body = obj.get()['Body'].read().decode('utf-8')
            print(key)
            for line in body.splitlines():
                json_data = json.loads(line)
                print(json_data['eventType'])
                print(json_data['mail']['destination'][0])
                
                if json_data['eventType'] == 'Bounce':
                    cnt_b += 1
                    bounce.append([json_data['mail']['destination'][0]])
                    #csv_writer.writerow([json_data['mail']['destination'][0], 'Bounce', json_data['bounce']['bounceType'], json_data['mail']['timestamp']])
                elif json_data['eventType'] == 'Complaint':
                    cnt_c += 1
                    complaint.append([json_data['mail']['destination'][0]])
                    #csv_writer.writerow([json_data['mail']['destination'][0], 'Complaint', json_data['mail']['timestamp']])
                elif json_data['eventType'] == 'Send':
                    cnt += 1
                    sent.append([json_data['mail']['destination'][0]])

    new = []
    bad = bounce + complaint

    for email in sent:
        if email not in bad and email not in new:
            new.append(email)
            csv_writer.writerow(email)
            print(len(new))
        else:
            print("bad")


    
    print('cnt')
    print(cnt)
    print('cnt_b')
    print(cnt_b)
    print('cnt_c')
    print(cnt_c)
    