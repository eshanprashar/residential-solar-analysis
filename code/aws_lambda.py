### Lambda function for generating embeddings of permit descriptions

import boto3
import json
from transformers import DistilBertTokenizer, DistilBertModel
import torch
from botocore.client import Config
from config import LAMBDA_INPUTS_FOLDER, S3_CLIENT, S3_RESOURCE, S3_BUCKET, S3_OUTPUTS_FOLDER, ROLE_ARN, IAM_CLIENT

# Function to generate embeddings
def get_embeddings(text):
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertModel.from_pretrained('distilbert-base-uncased')
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=200) # based on what we saw in the histogram
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Lambda function to process chunks
def lambda_handler(event,context):
    '''
    Read the file from local data folder
    Generate embeddings using the model
    Upload modified parquet to S3
    '''
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertModel.from_pretrained('distilbert-base-uncased')

    # Read the file from the local data folder
    parquet_file = event['file_name']
    chunk = pd.read_parquet(parquet_file)

    # Generate embeddings using the model
    chunk['embeddings'] = chunk['CLEAN_DESCRIPTION'].apply(lambda x: get_embeddings(x).tolist())

    # Save embeddings to S3
    try:
        output_file = parquet_file.replace('inputs', 'outputs')
        chunk.to_parquet(output_file)
        S3_CLIENT.upload_file(output_file, S3_BUCKET, S3_OUTPUTS_FOLDER + '/' + output_file.split('/')[-1])
        return {
            'statusCode': 200,
            'message': 'Embeddings generated and uploaded successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'message': 'Internal server error'
        }