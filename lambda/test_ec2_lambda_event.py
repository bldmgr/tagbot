"""EC2 Lambda unit tests."""
import unittest
import os.path
import json

from ec2_function import ec2_lambda_handler
from test_utils import attach_local_aws_response, ACCOUNT, REGION


class TestEC2(unittest.TestCase):
    """
    Test EC2 Lambda function.
    """
    def test_root_account(self):
        """
        Verify setting an EC2 tag when the creator is the root user.
        """
        with open('../test_event_data/ec2_root_account.json') as root_account:
            detail = json.load(root_account)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__), '../local-aws-response/root_account')
        attach_local_aws_response(path)
        self.assertEqual(ec2_lambda_handler(event, ''), True)

    def test_iam_user(self):
        """
        Verify setting an EC2 tag when the creator is a regular IAM user.
        """
        with open('../test_event_data/ec2_iam_user.json') as iam_user:
            detail = json.load(iam_user)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__), '../local-aws-response/iam_user')
        attach_local_aws_response(path)
        self.assertEqual(ec2_lambda_handler(event, ''), True)

    def test_create_volume(self):
        """
        Verify setting a tag on an EC2 volume creation event.
        """
        with open('../test_event_data/ec2_CreateVolume.json') as create_volume:
            detail = json.load(create_volume)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__), '../local-aws-response/create_volume')
        attach_local_aws_response(path)
        self.assertEqual(ec2_lambda_handler(event, ''), True)

    def test_create_snapshot(self):
        """
        Verify setting a tag on an EC2 snapshot creation event.
        """
        with open('../test_event_data/ec2_CreateSnapshot.json') as create_snapshot:
            detail = json.load(create_snapshot)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__), '../local-aws-response/create_snapshot')
        attach_local_aws_response(path)
        self.assertEqual(ec2_lambda_handler(event, ''), True)

    def test_start_instances(self):
        """
        Verify setting owner tag on an EC2 instance, volumes, and network interfaces
        when the interface is started.
        """
        with open('../test_event_data/ec2_StartInstances.json') as start_instances:
            detail = json.load(start_instances)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__), '../local-aws-response/start_instances')
        attach_local_aws_response(path)
        self.assertEqual(ec2_lambda_handler(event, ''), True)

    def test_reboot_instances(self):
        """
        Verify setting owner tag on an EC2 instance, volumes, and network interfaces
        when the interface is rebooted.
        """
        with open('../test_event_data/ec2_RebootInstances.json') as reboot_instances:
            detail = json.load(reboot_instances)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__), '../local-aws-response/reboot_instances')
        attach_local_aws_response(path)
        self.assertEqual(ec2_lambda_handler(event, ''), True)


if __name__ == '__main__':
    unittest.main()
