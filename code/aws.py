import json
import boto3
import os
from botocore.client import Config

# Load AWS credentials from the configuration file
with open('/Users/eshan23/eshanprashar_git_profile/residential-solar-analysis/data/aws_credentials/credentials.json') as f:
    aws_config = json.load(f)

# Set environment variables
os.environ['AWS_ACCESS_KEY_ID'] = aws_config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = aws_config['AWS_SECRET_ACCESS_KEY']
os.environ['AWS_DEFAULT_REGION'] = aws_config['AWS_DEFAULT_REGION']

# Initialize the clients for S3
s3 = boto3.client('s3', region_name=os.environ['AWS_DEFAULT_REGION'], config=Config(signature_version='s3v4'))
s3_resource = boto3.resource('s3')

bucket_name = 'solar-permits'

# Check if the S3 bucket exists; if not, create it
if 'Buckets' in s3.list_buckets():
    for bucket in s3.list_buckets()['Buckets']:
        if bucket['Name'] == bucket_name:
            print('S3 bucket exists')
            break
    else:
        s3.create_bucket(Bucket=bucket_name)