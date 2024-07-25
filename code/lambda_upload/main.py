try:
    import unzip_requirements
except ImportError:
    pass

import io
import os
import boto3
import torch
from transformers import DistilBertTokenizer, DistilBertModel
import pandas as pd

s3_resource = boto3.resource('s3')

# Function to generate embeddings
def get_embeddings(text):
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertModel.from_pretrained('distilbert-base-uncased')
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=200)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Lambda function to process chunks
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = event['bucket']
    key = event['key']

    # Download chunk from S3
    s3.download_file(bucket, key, '/tmp/data_chunk.parquet')
    chunk = pd.read_parquet('/tmp/data_chunk.parquet')

    # Generate embeddings using the model
    chunk['embeddings'] = chunk['CLEAN_DESCRIPTION'].apply(lambda x: get_embeddings(x).tolist())

    # Save embeddings to S3
    try:
        output_file = '/tmp/' + key.split('/')[-1].replace('inputs', 'outputs')
        chunk.to_parquet(output_file)
        s3.upload_file(output_file, bucket, 'permits-outputs/' + output_file.split('/')[-1])
        return {
            'statusCode': 200,
            'message': 'Embeddings generated and uploaded successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'message': str(e)
        }