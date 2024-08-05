import time
import grpc
import grpc.experimental.gevent as grpc_gevent

from grpc_interceptor import ClientInterceptor

# patch grpc so that it uses gevent instead of asyncio
grpc_gevent.init_gevent()

class Interceptor(ClientInterceptor):
    """
    A class representing an interceptor for gRPC client calls.
    Args:
        environment: The environment object.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    Attributes:
        env: The environment object.
    Methods:
        intercept: Intercepts the gRPC client call.
    """
        """
        Intercepts the gRPC client call.
        Args:
            method: The gRPC client method.
            request_or_iterator: The request or iterator object.
            call_details: The client call details.
        Returns:
            The response object.
        """
    def __init__(self, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.env = environment

    def intercept(
        
        self,
        method: callable,
        request_or_iterator: any,
        call_details: grpc.ClientCallDetails,
    ):
        """
        Intercepts a gRPC method call and performs additional actions.
        Args:
            method (callable): The gRPC method to be intercepted.
            request_or_iterator (any): The request or iterator object.
            call_details (grpc.ClientCallDetails): The call details of the gRPC method.
        Returns:
            any: The response object of the gRPC method call.
        """
        response = None
        result = None
        exception = None
        response_length = 0
        start_perf_counter = time.perf_counter()
        try:
            response = method(request_or_iterator, call_details)
            if not (type(response) == grpc._channel._MultiThreadedRendezvous):
                result = response.result()
        except grpc.RpcError as e:
            # Get the right response to handle an exception
            exception = e

        if type(response) == grpc._channel._MultiThreadedRendezvous:
            def cb_factory(exception, call_details, method_obj):
                def cb(response):
                    self.env.events.request.fire(
                        request_type="grpc",
                        name=call_details.method,
                        response_time=(time.perf_counter() - start_perf_counter) * 1000,
                        response_length=0,
                        response=response,
                        context=None,
                        exception=exception,
                        method=method_obj
                    )
                return cb
            cb = cb_factory(exception, call_details, method)
            response.add_done_callback(cb)
        else:
            if not (result == None):
                response_length = result.ByteSize()
            self.env.events.request.fire(
                request_type="grpc",
                name=call_details.method,
                response_time=(time.perf_counter() - start_perf_counter) * 1000,
                response_length=response_length,
                response=response,
                context=None,
                exception=exception,
                method=method
            )
        if not (exception == None):
            pass
        return response
