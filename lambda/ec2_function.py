"""EC2 tagging Lambda"""
import logging
from boto3wrapper import Boto3Wrapper
from utils import is_err_detail, get_creator, load_creator_tag

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def ec2_lambda_handler(event, context):
    """
    Assign owner tag to new EC2 resources.
    :param event: The incoming CloudTrail event object.
    :param context: This object provides methods and properties that provide information
    about the invocation, function, and execution environment.
    :return: True for non-error response events.
    """
    # print('event:', event)

    ids = []
    detail = event['detail']
    event_name = detail['eventName']
    creator = get_creator(event)

    ec2 = Boto3Wrapper.get_resource('ec2')

    if is_err_detail(logger, detail):
        return False

    if event_name == 'CreateVolume':
        ids.append(detail['responseElements']['volumeId'])
        logger.info(ids)
    elif event_name in ('RunInstances', 'StartInstances', 'RebootInstances'):
        ids = _load_instance_ids(detail, ec2, event_name)
        logger.info(ids)
        logger.info('number of instances: %d', len(ids))
    elif event_name == 'CreateImage':
        ids.append(detail['responseElements']['imageId'])
        logger.info(ids)
    elif event_name == 'CreateSnapshot':
        ids.append(detail['responseElements']['snapshotId'])
        logger.info(ids)
    else:
        logger.warning('Not supported action')

    if ids:
        for resource_id in ids:
            logger.info('resource id: %s', resource_id)
            ec2.create_tags(Resources=ids, Tags=[load_creator_tag(creator)])

    return True


def _load_instance_ids(detail, ec2, event_name):
    ids = []

    if event_name == 'RebootInstances':
        instance_loc = 'requestParameters'
    else:
        instance_loc = 'responseElements'
    items = detail[instance_loc]['instancesSet']['items']

    for item in items:
        ids.append(item['instanceId'])
    base = ec2.instances.filter(InstanceIds=ids)

    # loop through the instances
    for instance in base:
        for vol in instance.volumes.all():
            ids.append(vol.id)
        for eni in instance.network_interfaces:
            ids.append(eni.id)

    return ids
