# Audit IAM Access Keys and Prune


## Flow
1. Get all users
    1. Get each users access keys
        1. Check age of each access key
        2. If key age meets age limit
            1. If key is 'Inactive'
                1. Delete key
                2. log
            2. Else
                1. Update key to be 'Inactive'
                2. log
2. Publish to SNS

## Architecture


## Setup
```
aws s3 mb s3://$(BUCKET_NAME)
./deploy
```

### Test Local
- `export AWS_DEFAULT_PROFILE=$(profileName)`
- `python src/lambda_iam_keys_audit.py `
