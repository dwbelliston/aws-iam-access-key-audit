"""
AWS IAM ACCESS KEY AUDIT
"""
import datetime
import boto3

INACTIVE = 'Inactive'
MAX_KEY_AGE = 5
DELETE_KEY_WAITING_PERIOD = 5

KEYS_TO_DELETE = []
KEYS_TO_DEACTIVATE = []


def deactivate_keys(iam):
    if KEYS_TO_DEACTIVATE:
        for key in KEYS_TO_DEACTIVATE:
            response = iam.update_access_key(
                UserName=key['UserName'],
                AccessKeyId=key['AccessKeyId'],
                Status='Inactive'
            )

            print(response)

def delete_keys(iam):
    if KEYS_TO_DELETE:
        for key in KEYS_TO_DELETE:
            response = iam.delete_access_key(
                UserName=key['UserName'],
                AccessKeyId=key['AccessKeyId']
            )

            print(response)

def get_key_age(key_creation_date):
    """
    Return the Key Age of the user access key
    """
    now_date = datetime.datetime.now()
    now_date = now_date.replace(tzinfo=None)
    key_creation_date = key_creation_date.replace(tzinfo=None)
    date_diff = now_date - key_creation_date
    key_age = date_diff.days
    return key_age

def triage_key(key):
    key_age = get_key_age(key['CreateDate'])

    # Check key has aged past limit
    if key_age >= MAX_KEY_AGE:
        # Check it has aged past limit but already inactive
        if key['Status'] == INACTIVE:
            # Check we have waited long enough before we are safe to delete
            if key_age - MAX_KEY_AGE >= DELETE_KEY_WAITING_PERIOD:
                # Delete Key if we met the waiting period
                KEYS_TO_DELETE.append(key)
        else:
            # Key needs to be deactivated
            KEYS_TO_DEACTIVATE.append(key)

    # KEYS_TO_DEACTIVATE.append(key)

def process_users_keys(keys):
    if keys:
        for key in keys:
            triage_key(key)

def list_user_keys(iam, user):
    """
    Return all the access keys of the given user
    """
    keys = []
    paginator = iam.get_paginator('list_access_keys')
    for access_key in paginator.paginate(UserName=user['UserName']):
        for key in access_key['AccessKeyMetadata']:
            keys.append(key)
    return keys

def list_users(iam):
    """
    Return all AWS users list
    """
    users = []
    paginator = iam.get_paginator('list_users')
    for page_users in paginator.paginate():
        users.append(page_users)
    return users[0]['Users']


def handler():
    iam = boto3.client('iam')

    # Get the users for the account
    aws_users = list_users(iam)

    for aws_user in aws_users:
        if aws_user['UserName'] == 'dustin':
            # Get each users keys
            user_keys = list_user_keys(iam, aws_user)
            # Process the users keys
            process_users_keys(user_keys)
    
    delete_keys(iam)
    deactivate_keys(iam)

if __name__ == "__main__":
    boto3.setup_default_session(profile_name='1s-sandbox')
    handler()
