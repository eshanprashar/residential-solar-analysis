# Script to upload data to AWS S3 bucket, invoke lambda function to generate embeddings, and download the embeddings

import json
import boto3
import os
from botocore.client import Config
from config import S3_INPUTS_FOLDER, S3_CLIENT, S3_BUCKET, S3_OUTPUTS_FOLDER, AWS_LAMBDA


def upload_to_s3(file_path, bucket, key):
    S3_CLIENT.upload_file(file_path, bucket, key)
    print(f'Uploaded {file_path} to s3://{bucket}/{key}')

def invoke_lambda(function_name, payload):
    response = AWS_LAMBDA.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    response_payload = json.load(response['Payload'])
    return response_payload


def download_from_s3(bucket, key, download_path):
    S3_CLIENT.download_file(bucket, key, download_path)
    print(f'Downloaded s3://{bucket}/{key} to {download_path}')

def main():
    # Define S3 bucket and folder names
    input_file = os.path.join(S3_INPUTS_FOLDER, 'data_chunk_0.parquet')
    s3_input_key = 'permits-inputs/data_chunk_0.parquet'
    s3_output_key = 'permits-outputs/data_chunk_0.parquet'
    local_output_path = os.path.join(S3_OUTPUTS_FOLDER, 'data_chunk_0_embeddings.parquet')
    
    # Upload data chunk to S3
    try:
        upload_to_s3(input_file, S3_BUCKET, s3_input_key)
    except Exception as e:
        print(f'Error uploading {input_file} to S3: {e}')
        return

    # Invoke the Lambda function to generate embeddings
    payload = {
        'bucket': S3_BUCKET,
        'key': s3_input_key
    }
    lambda_name = 'embeddings'
    try:
        response = invoke_lambda(lambda_name, payload)
        print(response)
    except Exception as e:
        print(f'Error invoking Lambda function {lambda_name}: {e}')
        return

    if response['statusCode'] == 200:
        try:
            # Download the output file from S3 for further processing
            download_from_s3(S3_BUCKET, s3_output_key, local_output_path)
        except Exception as e:
            print(f'Error downloading output file from S3: {e}')
            return
if __name__ == '__main__':
    main()




    