class Device:
    """Represents a Device that receive Push Notifications"""
    type = None
    token = None

    def __init__(self, type, token):
        self.type = type
        self.token = token
