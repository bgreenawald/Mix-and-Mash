ENV_ZIP="env.zip"
ZIP_NAME="mix.zip"

rm $ZIP_NAME;
cp $ENV_ZIP $ZIP_NAME;

# Command to get all model directories
MODELS=$(find ./projects -type d -name "model")

# Add contexts of those directories to existing zip
zip -r $ZIP_NAME $MODELS lambda_function.py generate.py;

# Upload the new version of the package to lambda
aws s3 cp $ZIP_NAME s3://bhg5yd-lambda/mix-and-mash/$ZIP_NAME;
aws lambda update-function-code --function-name mix-and-mash --s3-bucket bhg5yd-lambda --s3-key mix-and-mash/$ZIP_NAME;