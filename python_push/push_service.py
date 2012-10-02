from abc import ABCMeta, abstractmethod


class PushService(object):
    """ Abstract class to represent a Push Service of a
        Mobile Platform"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def send_request(self, message, device_list):
        """ Return the request for Send a message to a especific PushService device list.

            message: The Message to be sent to the device list.
            device_list: A DeviceList with at least one Device.
        """
        pass

    @abstractmethod
    def send(self, message, device_list):
        """ Sends a message to a to a especific PushService device list and returns the Response.

            message: The Message to be sent to the device list.
            device_list: A DeviceList with at least oneDevice.
        """
        pass
