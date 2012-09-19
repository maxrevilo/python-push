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
        pass

    @abstractmethod
    def send(self, message, device, callback):
        pass
