# Step 1: Export Poetry dependencies to requirements.txt
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Step 2: Create deployment package directory
mkdir deployment_package

# Step 3: Install dependencies to deployment package directory
pip install -r requirements.txt -t deployment_package

# Step 4: Copy project files to deployment package directory
Get-ChildItem irrigation_handler -Recurse | Where-Object { $_.Name -ne '__pycache__' } | Copy-Item -Destination deployment_package -Recurse -Force

# Step 5: Zip the deployment package
Compress-Archive -Path deployment_package\* -DestinationPath deployment_package.zip

# Step 6: Deploy to AWS Lambda
aws lambda update-function-code --function-name your_lambda_function_name --zip-file fileb://deployment_package.zip
