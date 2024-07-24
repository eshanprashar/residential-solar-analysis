# Script to upload data to AWS S3 bucket, invoke lambda function to generate embeddings, and download the embeddings

import json
import boto3
import os
from botocore.client import Config
from config import S3_INPUTS_FOLDER, ROLE_ARN, S3_CLIENT, S3_RESOURCE, AWS_LAMBDA, LAMBDA_ZIP, IAM_CLIENT


def lambda_handler(event,context):





def main():
    # Define the S3 bucket and folder names
    bucket_name = 'solar-permits'
    folder_name = 'permits-inputs'
    # Check if the S3 bucket exists; if not, create it
    if 'Buckets' in S3_CLIENT.list_buckets():
        for bucket in S3_CLIENT.list_buckets()['Buckets']:
            if bucket['Name'] == bucket_name:
                print('S3 bucket exists')
                break
        else:
            S3_CLIENT.create_bucket(Bucket=bucket_name)
            print('S3 bucket created')

    # Invoke the Lambda function to generate embeddings
    

if __name__ == '__main__':
    main()




    