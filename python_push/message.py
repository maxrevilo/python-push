class Message:
    """ Represents a message to be sended to devices as a Push
        Notification."""
    payload = None
    options = {}

    def __init__(self):
        pass

    def set_option(self, key, value):
        pass

    def remove_option(self, key):
        pass

    def get_options(self):
        return self.options
