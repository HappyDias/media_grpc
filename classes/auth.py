import proto_classes.auth_service_pb2 as auth_service_pb2
from proto_classes.auth_service_pb2_grpc import AuthServiceStub
from google.protobuf.json_format import MessageToDict

from classes.channel import Channel

class Auth(Channel):
    """
    Auth class for handling authentication.
    Args:
        host (str): The host URL.
        email (str): The user's email.
        password (str): The user's password.
        interceptor: The interceptor object.
    Methods:
        sign_in_user(email, password): Signs in the user with the provided email and password.
    Returns:
        dict: The response message converted to a dictionary.
    """
    def __init__(self, host, email, password, interceptor):
        super().__init__(host, AuthServiceStub, interceptor=interceptor)
    
    def sign_in_user(self, email, password):
        """
        Signs in a user with the provided email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            dict: A dictionary containing the response message converted to a dictionary format.
        """
        response = self.stub.SignInUser(
            auth_service_pb2.rpc__signin__user__pb2.SignInUserInput(
                email=email,
                password=password
            )
        )
        return MessageToDict(response)