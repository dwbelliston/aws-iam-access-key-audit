# Audit IAM Access Keys and Prune


## Flow
1. Get all users
    1. Get each users access keys
        1. Check age of each access key
        2. If key age meets age limit
            1. If key is 'Inactive'
                1. Delete key
            2. Else
                1. Update key to be 'Inactive'
2. Send report

## Architecture


## Setup


## Misc
```
aws s3 mb s3://radius-audit

aws cloudformation package --template-file audit-api.cft.yml --s3-bucket radius-audit --output-template-file output.yml

aws cloudformation deploy --template-file output.yml --stack-name radius-audit --capabilities CAPABILITY_IAM
```



## Questions 

- which account will this live in? 1 in each account or can it do cross account?
- should boto3 client be a global for reuse?
- best way to handle sync/async (extreme case when need to delete 50 keys)
- best practice with cft