#!/bin/bash
source variables.sh

echo "Deleting Stack" $STACK_NAME

aws cloudformation delete-stack --stack-name $STACK_NAME