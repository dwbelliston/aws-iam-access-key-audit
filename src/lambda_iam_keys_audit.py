import time
import os
import logging
import datetime
import boto3

"""
LAMDBA IAM ACCESS KEY AUDIT

Check each access key for each user in the account and mark them as inactive when
they cross the max age limit. Keys will be deleted once they have been inactive for
a window of time.
"""

# Setup boto3
SESSION = boto3.session.Session()
IAM_CLIENT = boto3.client('iam')

# Setup Logger
LOGGER = logging.getLogger()
_log_handler = logging.StreamHandler()
_log_formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
_log_handler.setFormatter(_log_formatter)
LOGGER.addHandler(_log_handler)
LOGGER.setLevel(logging.INFO)

# Set up parameters
MAX_KEY_AGE_DAYS = float(os.environ.get('MAX_KEY_AGE_DAYS')) or 90
DELETE_KEY_WAITING_DAYS = os.environ.get('DELETE_KEY_WAITING_DAYS') or 5
INACTIVE = 'Inactive'
ACTIVE = 'Active'

# Buckets to hold keys that need action
KEYS_TO_DELETE = []
KEYS_TO_DEACTIVATE = []


def parse_api_response_code(response):
    try:
        response_status = response['ResponseMetadata']['HTTPStatusCode']
    except Exception as err:
        LOGGER.critical(err)
        response_status = None

    return response_status

def log_response(response, key, action):
    code_status = parse_api_response_code(response)

    if code_status == 200:
        LOGGER.info(
            f"{action} Key UserName={key['UserName']} AccessKeyId={key['AccessKeyId']} KeyAge={key['KeyAge']}")
    else:
        LOGGER.critical(
            f"Failed: {action} Key API={code_status} UserName={key['UserName']} AccessKeyId={key['AccessKeyId']} KeyAge={key['KeyAge']}")

def deactivate_keys():
    if KEYS_TO_DEACTIVATE:
        for key in KEYS_TO_DEACTIVATE:
            # Perform Action
            response = IAM_CLIENT.update_access_key(
                UserName=key['UserName'],
                AccessKeyId=key['AccessKeyId'],
                Status='Inactive'
            )

            # Log response
            log_response(response, key, 'Deactivated')


def delete_keys():
    if KEYS_TO_DELETE:
        for key in KEYS_TO_DELETE:
            response = IAM_CLIENT.delete_access_key(
                UserName=key['UserName'],
                AccessKeyId=key['AccessKeyId']
            )

            # Log response
            log_response(response, key, 'Deleted')


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


def format_key_object(key, key_age):
    return {
        'UserName': key['UserName'],
        'AccessKeyId': key['AccessKeyId'],
        'KeyAge': key_age
    }


def triage_key(key):
    '''
    Decide what action to take on the key based on age and status
    '''

    key_age = get_key_age(key['CreateDate'])

    # Check key has aged past limit
    if key_age >= MAX_KEY_AGE_DAYS:
        # Check it has aged past limit but already inactive
        if key['Status'] == INACTIVE:
            # Check we have waited long enough before we are safe to delete
            if key_age - MAX_KEY_AGE_DAYS >= DELETE_KEY_WAITING_DAYS:
                # Delete Key if we met the waiting period
                KEYS_TO_DELETE.append(format_key_object(key, key_age))
        elif key['Status'] == ACTIVE:
            # Key needs to be deactivated
            KEYS_TO_DEACTIVATE.append(format_key_object(key, key_age))


def process_users_keys(keys):
    '''
    Triage each key from the keys received
    '''
    if keys:
        for key in keys:
            triage_key(key)


def list_user_keys(user):
    """
    Return all the access keys of the given user
    """
    keys = []
    # TODO: Maybe dont need pagination, set flag to unpaginate
    paginator = IAM_CLIENT.get_paginator('list_access_keys')
    for access_key in paginator.paginate(UserName=user['UserName']):
        for key in access_key['AccessKeyMetadata']:
            keys.append(key)
    return keys


def list_users():
    """
    Return all AWS users list
    """
    users = []
    # TODO: Maybe dont need pagination, set flag to unpaginate
    paginator = IAM_CLIENT.get_paginator('list_users')
    for page_users in paginator.paginate():
        users.append(page_users)
    return users[0]['Users']


def lambda_handler(event, context):
    # Reset these to empty
    KEYS_TO_DELETE.clear()
    KEYS_TO_DEACTIVATE.clear()

    # Get the users for the account
    aws_users = list_users()

    for aws_user in aws_users:
        if aws_user['UserName'] == 'dustin':
            # Get each users keys
            user_keys = list_user_keys(aws_user)
            # Process the users keys
            process_users_keys(user_keys)
    
    delete_keys()
    deactivate_keys()


if __name__ == "__main__":
    '''
    Entry point when running localy, not needed when deployed
    '''
    event = []
    context = []
    lambda_handler(event, context)
