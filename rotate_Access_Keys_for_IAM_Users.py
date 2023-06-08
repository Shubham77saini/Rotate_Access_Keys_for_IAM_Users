#  Rotate Access Keys for IAM Users using CLI -- 

"""
List Accesskey information from AWSCLI 

aws configure

aws iam list-access-keys --user-name

Create Accesskey 
aws iam create-access-key --user-name username

Update Accesskey from AWSCLI
aws iam update-access-key --access-key-id accesskey --status Inactive --user-name username

delete Accesskey from awscli 
aws iam delete-access-key --access-key-id accesskeyhere --user-name username

"""


# -------------------------------------------------------------------------------------------------------------------------
# Never share Secret_key of your iam_user with any one.
#  Rotate Access Keys for IAM Users using boto3

import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

iam = boto3.resource('iam')

#------------------------------------------------------------------------------------------------------------------

def create_key(user_name):
    """
    Creates an access key for the specified user. Each user can have a
    maximum of two keys.
    :param user_name: The name of the user.
    :return: The created access key.
    """
    try:
        key_pair = iam.User(user_name).create_access_key_pair()
        logger.info(
            "Created access key pair for %s. Key ID is %s.",
            key_pair.user_name, key_pair.id)
    except ClientError:
        logger.exception("Couldn't create access key pair for %s.", user_name)
        raise
    else:
        return key_pair
    
res = create_key("user_admin_2")
print (res)

with open("new_access_id_and_password.txt", "w") as file:
    file.write(str(res))
# -----------------------------------------------------------------------------------------------

def get_last_use(key_id):
    """
    Gets information about when and how a key was last used.
    :param key_id: The ID of the key to look up.
    :return: Information about the key's last use.
    """
    try:
        response = iam.meta.client.get_access_key_last_used(AccessKeyId=key_id)
        last_used_date = response['AccessKeyLastUsed'].get('LastUsedDate', None)
        last_service = response['AccessKeyLastUsed'].get('ServiceName', None)
        logger.info(
            "Key %s was last used by %s on %s to access %s.", key_id,
            response['UserName'], last_used_date, last_service)
    except ClientError:
        logger.exception("Couldn't get last use of key %s.", key_id)
        raise
    else:
        return response
    
res = get_last_use("AKIA4HKVI64JGTO6NPTA")
print (res)

# -----------------------------------------------------------------------------------------------------------------

def list_keys(user_name):
    """
    Lists the keys owned by the specified user.
    :param user_name: The name of the user.
    :return: The list of keys owned by the user.
    """
    try:
        keys = list(iam.User(user_name).access_keys.all())
        logger.info("Got %s access keys for %s.", len(keys), user_name)
    except ClientError:
        logger.exception("Couldn't get access keys for %s.", user_name)
        raise
    else:
        return keys
    
res = list_keys ("user_admin_2")
print (res)

# #-------------------------------------------------------------------------------------------------

def update_key(user_name, key_id, activate):
    """
    Updates the status of a key.
    :param user_name: The user that owns the key.
    :param key_id: The ID of the key to update.
    :param activate: When True, the key is activated. Otherwise, the key is deactivated.
    """

    try:
        key = iam.User(user_name).AccessKey(key_id)
        if activate:
           key.activate()
        else:
            key.deactivate()
        logger.info("%s key %s.", 'Activated' if activate else 'Deactivated', key_id)
    except ClientError:
        logger.exception(
            "Couldn't %s key %s.", 'Activate' if activate else 'Deactivate', key_id)
        raise

res = update_key("user_admin_2", "AKIA4HKVI64JGTO6NPTA", False)
print (res)

# #----------------------------------------------------------------------------------------------------



# def update_key(user_name, key_id, activate):
#     """
#     Updates the status of a key.
#     :param user_name: The user that owns the key.
#     :param key_id: The ID of the key to update.
#     :param activate: When True, the key is activated. Otherwise, the key is deactivated.
#     """

#     try:
#         key = iam.User(user_name).AccessKey(key_id)
#         if activate:
#             key.activate()
#         else:
#             key.deactivate()
#         logger.info("%s key %s.", 'Activated' if activate else 'Deactivated', key_id)
#     except ClientError:
#         logger.exception(
#             "Couldn't %s key %s.", 'Activate' if activate else 'Deactivate', key_id)
#         raise

# res = update_key("user_demo", "AKIA4HKVI64JGTO6NPTA", True)
# print (res)

# #------------------------------------------------------------------------------------------------------------------


def delete_key(user_name, key_id):
    """
    Deletes a user's access key.
    :param user_name: The user that owns the key.
    :param key_id: The ID of the key to delete.
    """

    try:
        key = iam.AccessKey(user_name, key_id)
        key.delete()
        logger.info(
            "Deleted access key %s for %s.", key.id, key.user_name)
    except ClientError:
        logger.exception("Couldn't delete key %s for %s", key_id, user_name)
        raise

res = delete_key("user_admin_2", "AKIA4HKVI64JGTO6NPTA")
print (res)