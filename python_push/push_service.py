from abc import ABCMeta, abstractmethod


class PushService(object):
    """ Abstract class to represent a Push Service of a
        Mobile Platform"""

    __metaclass__ = ABCMeta

    """
    @abc.abstractmethod
    def __init__(self, settings):
        pass
    """

    @abstractmethod
    def register(self, token, callback):
        """ Register a device token validating it and
            generates a Device object.

            token: The device registration id.
            callback: the function to be executed when the registration completes
        """
        pass

    @abstractmethod
    def send(self, message, device, callback):
        pass
