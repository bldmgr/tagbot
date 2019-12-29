"""S3 Lambda unit tests."""
import unittest
import os.path
import json

from s3_function import s3_lambda_handler
from test_utils import attach_local_aws_response, ACCOUNT, REGION


class TestS3(unittest.TestCase):
    """
    Test S3 tagging Lambda function.
    """
    def test_create_s3_bucket(self):
        """
        Verifies setting an S3 Bucket Creator tag.
        """
        with open('../test_event_data/s3_CreateBucket.json') as s3_bucket:
            detail = json.load(s3_bucket)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__), '../local-aws-response/create_S3Bucket')
        attach_local_aws_response(path)
        self.assertEqual(s3_lambda_handler(event, ''), True)

    def test_put_s3_object(self):
        """
        Verifies setting an S3 Object Creator tag.
        Object uploaded by IAM user.
        """
        with open('../test_event_data/s3_PutObject.json') as s3_object:
            detail = json.load(s3_object)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__), '../local-aws-response/put_S3Object')
        attach_local_aws_response(path)
        self.assertEqual(s3_lambda_handler(event, ''), True)

    def test_put_s3_object_aws_service(self):
        """
        Verifies setting an S3 Object Creator tag.
        Object created by an AWS Service.
        """
        with open('../test_event_data/s3_PutObjectAWSService.json') as s3_object:
            detail = json.load(s3_object)
        event = {'account': ACCOUNT, 'region': REGION, 'detail': detail}
        path = os.path.join(os.path.dirname(__file__),
                            '../local-aws-response/put_S3ObjectAWSService')
        attach_local_aws_response(path)
        self.assertEqual(s3_lambda_handler(event, ''), True)


if __name__ == '__main__':
    unittest.main()
