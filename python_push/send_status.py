class SendStatus:
    """Represents a Push Service response to a push send request"""
    code = None
    success = None
    failure = None
    raw = None

    def __init__(self, code, success, failure, raw):
        self.code = code
        self.success = success
        self.failure = failure
        self.raw = raw
