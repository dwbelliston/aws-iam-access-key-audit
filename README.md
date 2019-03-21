# Audit IAM Access Keys and Prune


## Flow
1. Get all users
    1. Get each users access keys
        1. Check age of each access key
        2. If key age meets age limit
            1. If key is 'Inactive' and over waiting period for inactive keys
                1. Delete key
                2. log
            2. Else
                1. Update key to be 'Inactive'
                2. log
2. Publish to SNS

## Architecture


## Setup
- Need to have bucket created for cloud formation stack
- add the name to the `variables.sh` file
- update cloudformation template parameters
- run `./deploy.sh` to create stack