# Prep the artifact
./prep.sh

# Run cloudformation package and deploy
aws cloudformation package
--template-file aws-iam-keys-audit.cft.yml \
--s3-bucket aws-iam-keys-audit \
--output-template-file output.yml \
&& aws cloudformation deploy \
--template-file output.yml \
--stack-name stack-aws-iam-keys-audit \
--capabilities CAPABILITY_IAM\
