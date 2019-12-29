"""Redshift CloudWatch event Lambda unit tests."""
import unittest
import os.path
import json

from unittest.mock import patch
from redshift_function import redshift_lambda_handler
from redshift_sfn_function import redshift_sfn_lambda_handler
from test_utils import attach_local_aws_response, ACCOUNT, REGION


class TestRedshift(unittest.TestCase):
    """
    Test Redshift event handling Lambda function.
    """
    def test_create_cluster(self):
        """
        Verifies the Step Function state machine starts and the cluster is tagged.

        @return: True if asserts as expected
        """
        with open('../test_event_data/redshift_CreateCluster.json') as cluster:
            detail = json.load(cluster)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__),
                            '../local-aws-response/create_RedshiftCluster')
        attach_local_aws_response(path)
        with patch.dict(os.environ, {
                'SFN_MAX_RETRIES': '30',
                'SFN_ARN': 'arn:aws:states:us-east-1:292909299215:stateMachine:AutoTag-Redshift-SFN'
        }):
            self.assertEqual(redshift_lambda_handler(event, ''), True)

    def test_create_cluster_sfn_max_retries(self):
        """
        Verifies the event state when maximum retries have been reached.

        @return: True if the event response from the Lambda is as expected.
        """
        with open('../test_event_data/redshift_SFN_CreateCluster.json') as cluster:
            detail = json.load(cluster)
        attach_local_aws_response(path='')
        self.assertEqual(redshift_sfn_lambda_handler(detail, '')['TagStatus'],
                         'max retries reached')

    def test_create_cluster_sfn_complete(self):
        """
        Verifies the event state has status "complete" when tagging where retries remaining.

        @return: True if the event response from the Lambda is as expected.
        """
        with open('../test_event_data/redshift_SFN_CreateCluster.json') as cluster:
            detail = json.load(cluster)
        detail['MaxRetries'] = 10
        path = os.path.join(os.path.dirname(__file__),
                            '../local-aws-response/create_RedshiftCluster_SFN')
        attach_local_aws_response(path)
        self.assertEqual(redshift_sfn_lambda_handler(detail, '')['TagStatus'], 'complete')
