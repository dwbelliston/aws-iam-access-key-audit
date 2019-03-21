# AWS Lambda Audit IAM Access Keys and Prune
---
This template is used to create a CloudFormation Stack that implements a lambda function to audit iam access keys.

When keys reach the `MaxDaysAgeOfKey` they will be set to inactive. The keys will remain inactive, but will not be deleted until they age a specified number of days over the inactive threshold. This is done to allow time for applications to run and if any issues are encountered the key can quickly be activated again and the issue then handled. Once the key has been 'Inactive' for number of days to match `WaitDaysToDelete` they will then be deleted.

After this lambda runs it will track any successfull deactivations and deletions and report those keys to who ever is subscribed to the SNS topic defined in the stack.

<br />

## Application Flow
---
1. Get all users for the account
    1. Get each users access keys
        1. Check age of each access key against `MaxDaysAgeOfKey`
        2. If key age meets age limit
            1. Check if key is 'Inactive' and over waiting period defined by `WaitDaysToDelete`
                1. Key is Inactive and over the waiting period
                2. Mark key to be 'Deleted'
            2. Check if Key is 'Active'
                1. Key is 'Active' and is over the max age
                2. Mark key to be 'Deactivated'
2. Deactivate all keys that are marked to be deactivated
3. Delete all keys that are marked to be deleted
4. Publish all actions taken to SNS

<br />

## Getting Started
---
At a minimum, access to an AWS Account and permissions to deploy all of the resources defined in the template from the CloudFormation console are required. 

If you would like to deploy the template from the commandline a set of CLI credentials with the permissions to deploy all of the resources defined in the template and the installation and configuration of AWS CLI is required.

<br />

## Prerequisites
---
* Installing AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
* Configuring AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
* Create S3 bucket for cloud formation stack (aws cli):
  
        aws s3 mb <Stack Name>

<br />

## Deploying via AWS CLI
---
 Update the `parameters.json` file to store the template parameter values.

*Example*:
```
[
    "STACK_NAME=stack-lambda-iam-keys-audit",
    "STACK_BUCKET_NAME=stack-lambda-iam-keys-audit",
    "WaitDaysToDelete=90",
    "MaxDaysAgeOfKey=5",
    "ScheduleToRun=rate(1 day)",
    "SNSEmailSubscription=user@email.com"
]
```

Create the tags.json file and populate with all necessary tags.

*Example*:
```
[
    "Business_Unit=Security",
    "Owner=Owner",
    "Project=LambdaIamAudit"
]
```

Prepare the lambda artifact (this zips the function with its dependencies)
```
./prepare-lambda-artifact.sh
```

Package the cloud formation template
```
aws cloudformation package \
    --template-file cloudformation.yml \
    --s3-bucket <NAME OF STACK BUCKET> \
    --output-template-file output.yml \
```

Deploy the template to your account/environment:
```
aws cloudformation deploy \
    --template-file output.yml \
    --stack-name StackNameForIamAudit \
    --tags file://tags.json \
    --parameter-overrides file://parameters.json \
    --capabilities CAPABILITY_IAM
 ```

 <br />

## Quick Deploy
---
Run the `deploy.sh` command to run the `cloudformation package` and `cloudformation deploy` in one go
```
./deploy.sh
```

  <br />

## Deleting Stack via AWS CLI
---
Run the `delete-stack` command to tear down
```
aws cloudformation delete-stack --stack-name <STACK_NAME>
```

 <br />

 ## Authors
 ---
* [1Strategy](https://www.1strategy.com)

<br />

## License
---
Copyright 2019 1Strategy

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

<br />

## References
---
* Key Rotation Guidlines https://aws.amazon.com/blogs/security/how-to-rotate-access-keys-for-iam-users/
* AWS CloudFormation Best Practices: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html 
* AWS CloudFormation Template Reference: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-reference.html 
