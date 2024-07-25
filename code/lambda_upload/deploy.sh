#!/bin/bash

# Define the virtual environment and packages directory
VENV_DIR="../../venv"
PACKAGES_DIR="packages"

# Create the packages directory
mkdir -p $PACKAGES_DIR

# Copy the virtual environment packages
cp -r $VENV_DIR/lib/python3.11/site-packages/* $PACKAGES_DIR

# Change to the packages directory
cd $PACKAGES_DIR

# Remove unnecessary files and directories
find . -type d -name "tests" -exec rm -rf {} +
find . -type d -name "__pycache__" -exec rm -rf {} +
rm -rf ./{caffe2,wheel,wheel-*,pkg_resources,boto*,aws*,pip,pip-*,pipenv,setuptools}
rm -rf ./{*.egg-info,*.dist-info}
find . -name \*.pyc -delete

# Zip up torch
zip -r9 torch.zip torch
rm -r torch

# Zip everything up (including torch.zip)
zip -r9 ${OLDPWD}/pytorch_fn.zip .

# Change back to the lambda_upload directory
cd $OLDPWD/code/lambda_upload

# Add main.py and unzip_requirements.py to the ZIP file
zip -rg ${OLDPWD}/pytorch_fn.zip main.py unzip_requirements.py

# Change back to the original directory
cd $OLDPWD

# Clean up the packages directory
rm -r $PACKAGES_DIR

# Print the final ZIP file size (optional)
echo "Final ZIP file size:"
du -h pytorch_fn.zip
