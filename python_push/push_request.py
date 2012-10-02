from python_push.push_response import PushResponse


class PushRequest:
    """Represents a Push Service request for send a push"""
    type = None
    push_response = None
    on_response = None

    _request = None
    _response_builder = None

    def __init__(self, type, request, response_builder, on_response=None):
        """ Creates a PushRequest.
            type: The Push Service type of the request.
            request: The Python Request object (See PushService implementations)
            response_builder: A callback that receive the Python Response object and
                returns a PushResponse object.
            on_response: A callback to be executed after received the PushResponse (Optional).
        """
        self.type = type
        self.on_response = on_response
        self._request = request
        self._response_builder = response_builder

        def respone_handler(response):
            self.push_response = self._response_builder(response)
            assert isinstance(self.push_response, PushResponse)

            # Executing on_response Callback
            if self.on_response:
                on_response(self.push_response)

            return response

        self._request.hooks['response'] = respone_handler

    def send(self):
        """ Sends this PushRequest to the server and return the PushResponse """
        self._request.send()
        # Is supposed that the self.push_response is set on respone_handler
        return self.push_response
