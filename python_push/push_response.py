class PushResponse:
    """Represents a Push Service response to a push send request"""
    type = None
    code = None
    success = None
    failure = None
    raw = None
    description = None

    def __init__(self, type, code, raw='', description='', success=1, failure=0):
        """ Creates the PushResponse.
            type: The Push Service type of the response.
            code: The status code from the server.
            raw: The raw content of the response.

            ... Specific to Push Services implementations.
        """
        self.code = code
        self.success = success
        self.failure = failure
        self.raw = raw
        self.description = description
        self.type = type
