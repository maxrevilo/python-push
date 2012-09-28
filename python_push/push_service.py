from abc import ABCMeta, abstractmethod


class PushService(object):
    """ Abstract class to represent a Push Service of a
        Mobile Platform"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def send(self, message, device, callback):
        pass
