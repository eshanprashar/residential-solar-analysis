import os
import sys
import zipfile
import shutil
import boto3

# Define the paths
torch_dir = '/tmp/torch'
torch_zip_path = '/tmp/pytorch_fn/torch.zip'
s3_bucket_name = 'solar-permits'  # Replace with your bucket name
s3_key = 'pytorch_fn.zip'  # Replace with your S3 key

# Function to download the ZIP file from S3
def download_pytorch_fn_zip():
    s3 = boto3.client('s3')
    download_path = '/tmp/pytorch_fn.zip'
    
    # Download the file from S3
    s3.download_file(s3_bucket_name, s3_key, download_path)
    
    # Extract the pytorch_fn.zip to /tmp/pytorch_fn directory
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall('/tmp/pytorch_fn')

# Function to unzip the torch package
def unzip_torch():
    if not os.path.exists(torch_dir):
        tempdir = '/tmp/_torch'
        if os.path.exists(tempdir):
            shutil.rmtree(tempdir)
        zipfile.ZipFile(torch_zip_path, 'r').extractall(tempdir)
        os.rename(tempdir, torch_dir)
        sys.path.append(torch_dir)

# Execute the functions to download and unzip torch
download_pytorch_fn_zip()
unzip_torch()
