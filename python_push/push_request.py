from python_push.push_response import PushResponse
from asynchttp import Http


class PushRequest:
    """Represents a Push Service request for send a push"""
    type = None
    url = None
    body = None
    headers = None
    on_response = None
    response_builder = None

    _response_promise = None
    _push_response = None

    def __init__(self, type, url, body, headers, response_builder, on_response=None):
        """ Creates a PushRequest.
            type: The Push Service type of the request.
            url: is the URL push resource and can begin with either http or https.
            body: is the entity body to be sent with the request. It is a string object.
            headers: is a diccionary with extra headers that are to be sent with the request.
            response_builder: A callback that receive the Python Response object and
                returns a PushResponse object.
            on_response: A callback to be executed after received the PushResponse (Optional).
        """
        self.type = type
        self.url = url
        self.body = body
        self.headers = headers
        self.on_response = on_response
        self.response_builder = response_builder
        #Default response:
        self._push_response = PushResponse(type=self.type, code=0, is_ok=False, raw='Not sended')

    def send(self):
        """ Sends this PushRequest to the server and return the PushResponse """

        def respone_handler(promise):
            promise.response.text = str(promise.content)
            self._push_response = self.response_builder(promise.response)
            assert isinstance(self._push_response, PushResponse)

            # Executing on_response Callback
            if self.on_response:
                self.on_response(self._push_response)

            return promise.response

        self._response_promise, _ = Http().request(
            uri=self.url,
            method="POST",
            body=self.body,
            headers=self.headers,
            callback=respone_handler
        )

        return self

    def wait(self):
        """ After being sended wait until get the response. """
        if self._response_promise is not None:
            self._response_promise.wait()
        return self

    @property
    def push_response(self):
        return self.wait()._push_response
