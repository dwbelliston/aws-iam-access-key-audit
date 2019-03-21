# Add lambda src and libs together, then zip

# Remove any leftover assets from functions
rm -rf src/dist/*
rm src/lambda.zip

# Install lambda packages
pip install -r src/requirements.txt -t src/dist/

# Collect files into dist
cp src/lambda.py  src/dist

# Zip up the dist
cd src/dist
zip -r ../lambda.zip .