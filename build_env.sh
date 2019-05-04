# Ensure that the virtual environment is closed.
deactivate;

# Get calling path and zip path
CALL_DIR=$(pwd);
ZIP_FILE="env.zip"
ZIP_PATH="$CALL_DIR/$ZIP_FILE";

# Remove exising zip.
rm $ZIP_PATH;

# Zip the virtual environment.
cd env/lib/python3.6/site-packages/;
zip -r9 $ZIP_PATH .;

cd $CALL_DIR;
