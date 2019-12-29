"""Redshift creation queue reader Lambda"""
import logging
from botocore.exceptions import ClientError
from boto3wrapper import Boto3Wrapper

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def redshift_sfn_lambda_handler(event, context):
    """
    Assigns Creator tag to a new Redshift cluster, if the resource has completed creation.

    @param event: The input event from the Step Function state machine.
    @param context: Provides information about the invocation, function, and execution environment.
    @return: The event with possible update to 'Retries' and 'TagStatus'.
    'TagStatus' of "complete" or "max retries reached" cause the state machine to exit.
    """

    if event['MaxRetries'] <= event['Retries']:
        event['TagStatus'] = 'max retries reached'
        return event

    event['Retries'] = event['Retries'] + 1
    logging.info('Tag attempt for event: %s', event)

    redshift = Boto3Wrapper.get_client('redshift')

    try:
        redshift.create_tags(
            ResourceName=event['ResourceArn'],
            Tags=[
                {
                    'Key': 'Creator',
                    'Value': event['Creator']
                }
            ]
        )
        logging.info('Cluster has been tagged with Creator: %s', event['Creator'])
    except ClientError as error:  # fails when resource not ready
        logger.warning(error)
        return event

    event['TagStatus'] = 'complete'
    return event
