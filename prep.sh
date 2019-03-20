# Add lambda src and libs together, then zip

# Remove any leftover assets from functions
rm -rf src/dist/*
rm src/aws-iam-keys-audit.zip

# Install lambda packages
pip install -r src/requirements.txt -t src/dist/

# Collect files into dist
cp src/aws_iam_keys_audit.py  src/dist

# Zip up the dist
# zip -r src/aws-iam-keys-audit.zip src/dist
cd src/dist
zip -r ../aws-iam-keys-audit.zip .