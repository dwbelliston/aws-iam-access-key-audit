#!/bin/bash
STACK_NAME="stack-lambda-iam-keys-audit"
STACK_BUCKET_NAME="stack-lambda-iam-keys-audit"

# Prep the artifact
./prepare-lambda-artifact.sh

# Run cloudformation package and deploy
aws cloudformation package \
--template-file cloudformation.yml \
--s3-bucket $STACK_BUCKET_NAME \
--output-template-file output.yml \
&& aws cloudformation deploy \
--template-file output.yml \
--stack-name $STACK_NAME \
--tags file://tags.json \
--parameter-overrides file://parameters.json \
--capabilities CAPABILITY_IAM
