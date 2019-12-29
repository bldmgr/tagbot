"""A place for common test utility functions."""
import placebo

from boto3wrapper import Boto3Wrapper

MODE = ['playback', 'record']
ACCOUNT = '2523223215'
REGION = 'us-east-1'


class MockContext:
    """
    Mock the AWS Python SDK Lambda context.
    @see https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    """
    def __init__(self, ttl):
        self.ttl = ttl

    def get_remaining_time_in_millis(self):
        """
        Mocks the time remaining in milliseconds before Lambda execution time out.
        @return: Fixed 60ms
        """
        return self.ttl

    def get_ttl(self):
        """
        Dummy method to avoid RO903: too-few-public-methods
        @return: ttl
        """
        return self.ttl


def attach_local_aws_response(path, mode='playback'):
    """
    Provide a mock AWS response. Steps:
    1) Create or re-create a session.
    2) Bind the session to the mock API.
    3) Play the mock data.
    :param path: The location of the mock data.
    :param mode: Placebo runtime mode, playback(default) or record.
    """
    session = Boto3Wrapper.get_session()
    pill = placebo.attach(session, data_path=path)
    Boto3Wrapper.SESSION_CREATE_HOOK = session
    if mode == 'playback':
        pill.playback()
    else:
        pill.record()
