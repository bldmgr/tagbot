""" AWS SDK client, session, resource wrapper """
import boto3


class Boto3Wrapper:
    """A wrapper class over the AWS SDK for Python - Boto 3"""

    SESSION_CREATION_HOOK = None

    @classmethod
    def get_session(cls):
        """Create or re-create an AWS session."""

        session = boto3.Session(region_name='us-east-1')
        cls.SESSION_CREATION_HOOK = session
        return session

    @classmethod
    def get_resource(cls, aws_resource):
        """
        Get the AWS resource from the session, or create from
        the default session it if there is no session.
        """
        if cls.SESSION_CREATION_HOOK is None:
            resource = boto3.resource(aws_resource)
        else:
            session = cls.SESSION_CREATION_HOOK
            resource = session.resource(aws_resource)
        return resource

    @classmethod
    def get_client(cls, aws_resource):
        """
        Get the client from the session, or create a low-level
        service client from the default session.
        """
        if cls.SESSION_CREATION_HOOK is None:
            resource = boto3.client(aws_resource)
        else:
            session = cls.SESSION_CREATION_HOOK
            resource = session.client(aws_resource)

        return resource
