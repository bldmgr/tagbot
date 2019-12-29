"""RDS Lambda unit tests."""
import unittest
import os.path
import json

from rds_function import rds_lambda_handler
from test_utils import attach_local_aws_response, ACCOUNT, REGION


class TestRDS(unittest.TestCase):
    """
    Test RDS Lambda function.
    """
    def test_create_db_subnet_group(self):
        """
        Verify setting a tag on a subnet group creation event.
        """
        with open('../test_event_data/rds_CreateDBSubnetGroup.json') as db_subnet_group:
            detail = json.load(db_subnet_group)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__), '../local-aws-response/create_DBSubnetGroup')
        attach_local_aws_response(path)
        self.assertEqual(rds_lambda_handler(event, ''), True)

    def test_create_db_parameter_group(self):
        """
        Verify setting a tag on a DB parameter group creation event.
        """
        with open('../test_event_data/rds_CreateDBParameterGroup.json') as db_param_group:
            detail = json.load(db_param_group)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__),
                            '../local-aws-response/create_DBParameterGroup')
        attach_local_aws_response(path)
        self.assertEqual(rds_lambda_handler(event, ''), True)

    def test_create_option_group(self):
        """
        Verify setting a tag on a option group creation event.
        """
        with open('../test_event_data/rds_CreateOptionGroup.json') as option_group:
            detail = json.load(option_group)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__), '../local-aws-response/create_DBOptionGroup')
        attach_local_aws_response(path)
        self.assertEqual(rds_lambda_handler(event, ''), True)

    def test_create_db_instance(self):
        """
        Verify setting a tag on a DB instance creation event.
        """
        with open('../test_event_data/rds_CreateDBInstance.json') as db_instance:
            detail = json.load(db_instance)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__), '../local-aws-response/create_DBInstance')
        attach_local_aws_response(path)
        self.assertEqual(rds_lambda_handler(event, ''), True)

    def test_create_db_cluster_snapshot(self):
        """
        Verify setting a tag on a DB cluster snapshot creation event.
        """
        with open('../test_event_data/rds_CreateDBClusterSnapshot.json') as db_cluster_snapshot:
            detail = json.load(db_cluster_snapshot)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__),
                            '../local-aws-response/create_DBClusterSnapshot')
        attach_local_aws_response(path)
        self.assertEqual(rds_lambda_handler(event, ''), True)


if __name__ == '__main__':
    unittest.main()
