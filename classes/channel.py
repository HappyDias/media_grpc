import grpc

class Channel():
    """
    Represents a channel for communication with a gRPC server.
    Args:
        host (str): The host address of the gRPC server.
        stub_class (class): The class representing the gRPC stub.
        interceptor (object, optional): An interceptor object for intercepting gRPC calls. Defaults to None.
    """
    def __init__(self, host, stub_class, interceptor=None):
        self._channel = grpc.insecure_channel(host)
        if interceptor:
            self._channel = grpc.intercept_channel(self._channel, interceptor)

        self.stub = stub_class(self._channel)