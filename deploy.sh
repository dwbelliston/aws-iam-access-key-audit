./prep.sh
aws cloudformation package --template-file audit-api.cft.yml --s3-bucket radius-mailing --output-template-file output.yml && aws cloudformation deploy --template-file output.yml --stack-name radius-audit-1 --capabilities CAPABILITY_IAM
