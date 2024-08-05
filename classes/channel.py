import grpc

class Channel():
    def __init__(self, host, stub_class, interceptor=None):
        self._channel = grpc.insecure_channel(host)
        if interceptor:
            self._channel = grpc.intercept_channel(self._channel, interceptor)

        self.stub = stub_class(self._channel)