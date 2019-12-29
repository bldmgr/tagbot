"""A place for common utility functions."""

CREATOR_TAG_NAME = 'Creator'


def is_err_detail(logger, detail, expect_resp_elems=True):
    """
    Checks if the event detail represents an error.

    :param logger: The application logger.
    :param detail: The detail portion of the CloudTrail object.
    :param expect_resp_elems: If true consider not response elements an error state.
    :return: True if the detail represents an error event.
    """
    error = False
    if expect_resp_elems and 'responseElements' not in detail:
        logger.error('The event detail does not contain responseElements')
        error = True
    if 'errorCode' in detail:
        logger.error('errorCode: %s', detail['errorCode'])
        error = True
    if 'errorMessage' in detail:
        logger.error('errorMessage: %s', detail['errorMessage'])
        error = True
    return error


def get_creator(event):
    """
    Get the user or AWS service from the event data. Creator is set to:
        o IAM User - user name
        o Root - hard coded to root_account
        o AWS Service - the service created the resource
        o All others - principal ID (same as IAM owner ID)
        o All else fails - undetermined

    TODO - Are all user identity types handled?
    https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html

    :param event: The CloudTrail event object.
    :return: The creator.
    """
    detail = event['detail']
    user_type = detail['userIdentity']['type']

    if user_type == 'IAMUser':
        user = detail['userIdentity']['userName']
    elif user_type == 'Root':
        user = "root_account"
    elif user_type == 'AWSService':
        user = detail['userIdentity']['invokedBy']
    else:
        if 'principalId' in detail:
            user = detail['userIdentity']['principalId']
        else:
            user = 'undetermined'

    return user


def load_creator_tag(creator):
    """
    Initialize the Creator tag.
    :param creator: The owner name, root_account, or AWS service creating the resource.
    :return: The tag dict.
    """
    tag = {
        'Key': CREATOR_TAG_NAME,
        'Value': creator
    }
    return tag
