import os
import sys
import zipfile
import shutil
import boto3
import time

# Define the paths
torch_dir = '/tmp/torch'
s3_bucket_name = 'solar-permits'  # Replace with your bucket name
s3_key = 'pytorch_fn.zip'  # Replace with your S3 key

# Function to download the ZIP file from S3
def download_pytorch_fn_zip():
    s3 = boto3.client('s3')
    download_path = '/tmp/pytorch_fn.zip'
    
    print("Downloading pytorch_fn.zip from S3...")
    start_time = time.time()
    s3.download_file(s3_bucket_name, s3_key, download_path)
    end_time = time.time()
    print(f"Download completed in {end_time - start_time} seconds")
    
    # Extract the pytorch_fn.zip to /tmp/pytorch_fn directory
    print("Extracting pytorch_fn.zip...")
    start_time = time.time()
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall('/tmp/pytorch_fn')
    end_time = time.time()
    print(f"Extraction completed in {end_time - start_time} seconds")

    # List the contents of /tmp/pytorch_fn to verify
    extracted_files = os.listdir('/tmp/pytorch_fn')
    print(f"Contents of /tmp/pytorch_fn: {extracted_files}")

# Function to unzip all contents and set up environment variables
def setup_environment():
    # Move all contents of /tmp/pytorch_fn to /tmp/
    for item in os.listdir('/tmp/pytorch_fn'):
        s = os.path.join('/tmp/pytorch_fn', item)
        d = os.path.join('/tmp', item)
        if os.path.isdir(s):
            shutil.move(s, d)
        else:
            shutil.copy2(s, d)

    # Set environment variables for shared libraries
    lib_dir = '/tmp/torch/lib'
    os.environ['LD_LIBRARY_PATH'] = f"{lib_dir}:{os.environ.get('LD_LIBRARY_PATH', '')}"
    print(f"LD_LIBRARY_PATH set to: {os.environ['LD_LIBRARY_PATH']}")
    sys.path.append('/tmp')
    print(f"sys.path updated to include /tmp")

# Execute the functions to download and set up the environment
download_pytorch_fn_zip()
setup_environment()