"""Redshift creation event Lambda handler"""
import json
import logging
import os
from boto3wrapper import Boto3Wrapper
from utils import is_err_detail, get_creator

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def redshift_lambda_handler(event, context):
    """
    Fires on Redshift cluster creation, parses the event, starts and passes event summary to
    the Step Function state machine that will arrange for the Creator tag to be added.

    :param event: The CloudWatch event.
    :param context: Provides information about the invocation, function, and execution environment.
    :return: True if the input event is not describing an error.
    """
    logging.debug('event: %s', event)

    detail = event['detail']
    event_name = detail['eventName']
    creator = get_creator(event)

    logger.info('Event type: %s', event_name)

    if is_err_detail(logger, detail):
        return False

    if event_name == 'CreateCluster':
        logger.debug('%s is creating cluster: %s',
                     creator, detail['requestParameters']['clusterIdentifier'])

        # https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
        cluster_arn = 'arn:aws:redshift:' + detail['awsRegion'] + ':'\
                      + detail['userIdentity']['accountId'] + ':cluster:'\
                      + detail['requestParameters']['clusterIdentifier']
        short_msg = {
            "EventName": event_name,
            "Creator": creator,
            "ResourceArn": cluster_arn,
            "TagStatus": "pending",
            "MaxRetries": int(os.environ['SFN_MAX_RETRIES']),
            "Retries": 0
        }

        sfn = Boto3Wrapper.get_client('stepfunctions')
        response = sfn.start_execution(
            stateMachineArn=os.environ['SFN_ARN'],
            name=creator+'-'+event_name+'-'+detail['eventID'],
            input=json.dumps(short_msg)
        )

        logger.info('Step Functions start execution: %s', response)

    return True
