#!/usr/bin/env python

import boto3
import json

# Check AMI ID in servicetypes.json file
with open("./JSON_FILE.example.json", "r") as json_file:
        servicetypes = json.load(json_file)
        a = servicetypes['JSON_KEY']                                    # The json key that contains the ami property. In my case it was the name of the EC2 service that needed to use the ami.
        ami_id = a['ami']
        print('JSON_FILE.example.json file has the following AMI: ', ami_id)

# Read S3 txt file content
s3 = boto3.client('s3')
s3_file = s3.get_object(Bucket='S3_BUCKET',Key='ami.txt')               # The CI/CD pipeline uploads this ami.txt file in s3.

filedata = s3_file['Body'].read()
s3_content = filedata.decode('utf-8')
s3_ami_Id = s3_content.strip('\n')
print('The s3 txt file has the following AMI:', s3_ami_Id)
print('===========================')

# Check and change servicetypes.json file
if ami_id == s3_ami_Id:
    print('No new AMI, nothing to be done.')
else:
    print('Detected a new AMI for in S3, changing ' + ami_id + ' with ' + s3_ami_Id)
    with open("./JSON_FILE.example.json", "r+") as json_file:
        servicetypes = json.load(json_file)
           
        for i in servicetypes:
            if 'type' in servicetypes[i]:
                if servicetypes[i]['type'] == 'linux-browser':          # A string to check against. In my case I had the key `type` set in the JSON file in the keys that I needed to update the AMI for. The others (other type or no type at all) will be skipped.
                    
                    servicetypes[i]['ami'] = s3_ami_Id

                    json_file.seek(0)
                    json.dump(servicetypes, json_file, indent=4, sort_keys=True)
                    json_file.truncate()
                else:
                    continue
            else:
                continue
    print('Done! All linux-browsers AMIs changed.')