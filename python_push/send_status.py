class SendStatus:
    """Represents a Push Service response to a push send request"""
    code = None
    success = None
    failure = None
    raw = None
    description = None

    def __init__(self, code, raw='', description='', success=1, failure=0):
        self.code = code
        self.success = success
        self.failure = failure
        self.raw = raw
        self.description = description
