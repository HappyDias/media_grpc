import proto_classes.auth_service_pb2 as auth_service_pb2
from proto_classes.auth_service_pb2_grpc import AuthServiceStub
from google.protobuf.json_format import MessageToDict

from classes.channel import Channel

class Auth(Channel):
    def __init__(self, host, email, password, interceptor):
        super().__init__(host, AuthServiceStub, interceptor=interceptor)
    
    def sign_in_user(self, email, password):
        response = self.stub.SignInUser(
            auth_service_pb2.rpc__signin__user__pb2.SignInUserInput(
                email=email,
                password=password
            )
        )
        return MessageToDict(response)