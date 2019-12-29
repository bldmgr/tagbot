"""S3 tagging Lambda"""
import logging
from botocore.exceptions import ClientError
from boto3wrapper import Boto3Wrapper
from utils import is_err_detail, get_creator, load_creator_tag

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Event types
BUCKET_EVENTS = ['CreateBucket']
OBJECT_EVENTS = ['PutObject']


def s3_lambda_handler(event, context):
    """
    Assign owner tag to new buckets and objects added to buckets. Object creation event
    notification is added to new buckets.

    :param event: The incoming CloudTrail event object.

    :param context: This object provides methods and properties that provide information
    about the invocation, function, and execution environment.
    See https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    :return: True for non-error response events.
    """
    # print('event:', event)

    detail = event['detail']
    event_name = detail['eventName']
    bucket_name = detail['requestParameters']['bucketName']
    creator = get_creator(event)

    logger.info('email: %s', creator)
    logger.info('bucket name: %s', bucket_name)

    # gets an S3.Client object
    s3 = Boto3Wrapper.get_client('s3')

    if is_err_detail(logger, detail, expect_resp_elems=False):
        return False

    tag_set = {
        'TagSet': [load_creator_tag(creator)]
    }

    if event_name in BUCKET_EVENTS:
        logger.info('adding bucket Creator tag: [ %s ] to bucket [ %s ]',
                    creator, bucket_name)
        try:
            logger.info('tagging bucket')
            s3.put_bucket_tagging(
                Bucket=bucket_name,
                Tagging=tag_set
            )
        except ClientError as error:
            logger.error(error)
            return False
    elif event_name in OBJECT_EVENTS:
        object_key = detail['requestParameters']['key']
        logger.info('adding object Creator tag: [ %s ] to bucket [ %s ] object [ %s ]',
                    creator, bucket_name, object_key)
        try:
            s3.put_object_tagging(
                Bucket=bucket_name,
                Key=object_key,
                Tagging=tag_set
            )
        except ClientError as error:
            logger.error(error)
            return False
    else:
        logger.warning('Not supported action: %s', event_name)
        return False

    return True
