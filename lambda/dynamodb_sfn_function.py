"""DynamoDB and DAX tagging Lambda"""
import logging
from botocore.exceptions import ClientError
from boto3wrapper import Boto3Wrapper
from utils import load_creator_tag

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def dynamodb_sfn_handler(event, context):
    """
    Lambda function that is called by the DynamoDB Step Function state machine.
    It attempts to tag the resource specified in the incoming event.

    :param event: The incoming state machine event object.

    :param context: This object provides methods and properties that provide information
    about the invocation, function, and execution environment.
    See https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    @return: The event to the state machine. TagStatus and Attempts can be changed.
    When the resource is tagged, TagStatus is set to "completed". Attempts increment
    each time this Lambda is called.
    """

    if event['MaxAttempts'] <= event['Attempts']:
        event['TagStatus'] = 'max attempts reached'
        return event

    event['Attempts'] = event['Attempts'] + 1
    logging.info('Tag attempt for event: %s', event)

    if event['EventName'] == 'CreateTable':
        try:
            dynamodb = Boto3Wrapper.get_client('dynamodb')
            dynamodb.tag_resource(
                ResourceArn=event['ResourceArn'],
                Tags=[load_creator_tag(event['Creator'])]
            )
            logging.info('Table has been tagged.')
        except ClientError as error:  # fails when resource not ready
            logger.warning(error)
            return event
    elif event['EventName'] == 'CreateCluster':
        try:
            dax = Boto3Wrapper.get_client('dax')
            dax.tag_resource(
                ResourceName=event['ResourceArn'],
                Tags=[load_creator_tag(event['Creator'])]
            )
            logging.info('Cluster has been tagged')
        except ClientError as error:  # fails when resource not ready
            logger.warning(error)
            return event
    else:
        event['TagStatus'] = 'unsupported event'
        return event

    event['TagStatus'] = 'complete'
    return event
