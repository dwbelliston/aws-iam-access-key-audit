#!/bin/bash
source variables.sh

# Prep the artifact
./prep.sh

# Run cloudformation package and deploy
aws cloudformation package \
--template-file cloudformation.yml \
--s3-bucket $STACK_BUCKET_NAME \
--output-template-file output.yml \
&& aws cloudformation deploy \
--template-file output.yml \
--stack-name $STACK_NAME \
--capabilities CAPABILITY_IAM\
