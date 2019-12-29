"""RDS tagging Lambda"""
import logging
from boto3wrapper import Boto3Wrapper
from utils import is_err_detail, get_creator, load_creator_tag

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def rds_lambda_handler(event, context):
    """
    Assign owner tag to new RDS resources
    :param event: The incoming CloudTrail event object.
    :param context: This object provides methods and properties that provide information
    about the invocation, function, and execution environment.
    :return: True for non-error response events.
    """
    resource_arn = None
    detail = event['detail']
    event_name = detail['eventName']
    creator = get_creator(event)

    rds = Boto3Wrapper.get_client('rds')

    if is_err_detail(logger, detail):
        return False

    if event_name == 'CreateDBInstance':
        resource_arn = detail['responseElements']['dBInstanceArn']
    elif event_name == 'CreateDBSnapshot':
        resource_arn = detail['responseElements']['dBSnapshotArn']
    elif event_name == 'CreateDBClusterSnapshot':
        resource_arn = detail['responseElements']['dBClusterSnapshotArn']
    elif event_name == 'CreateDBParameterGroup':
        resource_arn = detail['responseElements']['dBParameterGroupArn']
    elif event_name == 'CreateDBSubnetGroup':
        resource_arn = detail['responseElements']['dBSubnetGroupArn']
    elif event_name == 'CreateOptionGroup':
        resource_arn = detail['responseElements']['optionGroupArn']
    else:
        logger.warning('Not supported action')

    if resource_arn:
        rds.add_tags_to_resource(
            ResourceName=resource_arn, Tags=[load_creator_tag(creator)]
        )

    return True
