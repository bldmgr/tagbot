"""DynamoDB creation event Lambda handler"""
import json
import logging
import os
from boto3wrapper import Boto3Wrapper
from utils import is_err_detail, get_creator

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def dynamodb_cloudwatch_handler(event, context):
    """
    Lambda function that responds to DynamoDB create table and create cluster
    CloudWatch events via EventBridge triggers. The event is processed,
    summarized and becomes input to the DynamoDB Step Function state machine
    that is started to manage the resource tagging.

    :param event: The incoming CloudWatch event object.

    :param context: This object provides methods and properties that provide information
    about the invocation, function, and execution environment.
    See https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    @return: True if the state machine execution started or False if the
    event represents an error.
    """
    logger.debug('event: %s', event)

    detail = event['detail']
    event_name = detail['eventName']
    creator = get_creator(event)

    logger.info('Event type: %s', event_name)

    if is_err_detail(logger, detail):
        return False

    sfn_event = {
        "EventName": event_name,
        "Creator": creator,
        "ResourceArn": "",
        "TagStatus": "pending",
        "MaxAttempts": int(os.environ['SFN_MAX_ATTEMPTS']),
        "Attempts": 0
    }

    if event_name == 'CreateTable':
        sfn_event['ResourceArn'] = detail['responseElements']['tableDescription']['tableArn']
        logger.info('Table [ %s ] requires tag Creator [ %s ]',
                    sfn_event['ResourceArn'], creator)
    elif event_name == 'CreateCluster':
        sfn_event['ResourceArn'] = detail['responseElements']['cluster']['clusterArn']
        logger.info('Cluster [ %s ] requires tag Creator [ %s ]',
                    sfn_event['ResourceArn'], creator)
    else:
        logger.warning('Event [ %s ] is not supported', event_name)
        return False

    sfn = Boto3Wrapper.get_client('stepfunctions')
    response = sfn.start_execution(
        stateMachineArn=os.environ['SFN_ARN'],
        name=creator+'-'+event_name+'-'+detail['eventID'],
        input=json.dumps(sfn_event)
    )

    logger.info('Step Functions start execution: %s', response)

    return True
