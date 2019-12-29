"""DynamoDB and DAX Lambda unit tests."""
import unittest
import os.path
import json

from unittest.mock import patch
from dynamodb_cloudwatch_function import dynamodb_cloudwatch_handler
from dynamodb_sfn_function import dynamodb_sfn_handler
from test_utils import attach_local_aws_response, ACCOUNT, REGION


class TestDynamoDB(unittest.TestCase):
    """
    Test DynamoDB event handling and SFN Lambda function.
    """
    def test_create_table_start_state_machine(self):
        """
        Verifies the Step Function state machine starts when receiving a
        create table CloudWatch event.

        @return: True if the Lambda returns True.
        """
        with open('../test_event_data/dynamodb_CreateTable.json') as table:
            detail = json.load(table)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__),
                            '../local-aws-response/create_DynamoDBTable')
        attach_local_aws_response(path)
        with patch.dict(os.environ, {
                'SFN_MAX_ATTEMPTS': '30',
                'SFN_ARN': 'arn:aws:states:us-east-1:292909299215:stateMachine:AutoTag-DynamoDB-SFN'
        }):
            self.assertEqual(dynamodb_cloudwatch_handler(event, ''), True)

    def test_create_table_sfn_max_attempts(self):
        """
        Verifies the table event state when maximum attempts have been reached.

        @return: True if the event response from the Lambda has the proper tag status.
        """
        with open('../test_event_data/dynamodb_SFN_CreateTable.json') as sfn_event:
            detail = json.load(sfn_event)
        attach_local_aws_response(path='')
        self.assertEqual(dynamodb_sfn_handler(detail, '')['TagStatus'],
                         'max attempts reached')

    def test_create_table_sfn_complete(self):
        """
        Verifies the table event state has status "complete" when resource is tagged.

        @return: True if the event response from the Lambda has the proper tag status.
        """
        with open('../test_event_data/dynamodb_SFN_CreateTable.json') as sfn_event:
            detail = json.load(sfn_event)
        detail['MaxAttempts'] = 10
        detail['Attempts'] = 0
        path = os.path.join(os.path.dirname(__file__),
                            '../local-aws-response/create_DynamoDBTable_SFN')
        attach_local_aws_response(path)
        self.assertEqual(dynamodb_sfn_handler(detail, '')['TagStatus'], 'complete')

    def test_create_cluster_start_state_machine(self):
        """
        Verifies the Step Function state machine starts when receiving
        a create cluster CloudWatch event.

        @return: True if the Lambda returns True.
        """
        with open('../test_event_data/dynamodb_DAX_CreateCluster.json') as cluster:
            detail = json.load(cluster)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__),
                            '../local-aws-response/create_DynamoDBDAXCluster')
        attach_local_aws_response(path)
        with patch.dict(os.environ, {
                'SFN_MAX_ATTEMPTS': '30',
                'SFN_ARN': 'arn:aws:states:us-east-1:292909299215:stateMachine:AutoTag-DynamoDB-SFN'
        }):
            self.assertEqual(dynamodb_cloudwatch_handler(event, ''), True)

    def test_create_cluster_sfn_max_attempts(self):
        """
        Verifies the cluster event state when maximum attempts have been reached.

        @return: True if the event response from the Lambda has the proper tag status.
        """
        with open('../test_event_data/dynamodb_SFN_CreateCluster.json') as sfn_event:
            detail = json.load(sfn_event)
        detail['MaxAttempts'] = 10
        detail['Attempts'] = 10
        attach_local_aws_response(path='')
        self.assertEqual(dynamodb_sfn_handler(detail, '')['TagStatus'],
                         'max attempts reached')

    def test_create_cluster_sfn_complete(self):
        """
        Verifies the cluster event state has status "complete" when resource is tagged.

        @return: True if the event response from the Lambda has the proper tag status.
        """
        with open('../test_event_data/dynamodb_SFN_CreateCluster.json') as sfn_event:
            detail = json.load(sfn_event)
        detail['MaxAttempts'] = 10
        detail['Attempts'] = 0
        path = os.path.join(os.path.dirname(__file__),
                            '../local-aws-response/create_DynamoDBCluster_SFN')
        attach_local_aws_response(path)
        self.assertEqual(dynamodb_sfn_handler(detail, '')['TagStatus'], 'complete')
