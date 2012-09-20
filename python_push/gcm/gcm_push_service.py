from python_push.push_service import PushService
from python_push.device import Device
from python_push.send_status import SendStatus


class GCMPushService(PushService):
    """GCM Push Service implementation"""
    settings = None
    type = "ANDROID"

    def __init__(self, settings):
        """ Initializes the GCM Push Service with the specified settings.
            settings: {
                api_id: Google Server API Key.

                defaults: The options applied to an push if they are not specified.
                {
                    collapse_key: ...
                    delay_while_idle: ...
                    time_to_live: ...
                }
            }
        """
        if 'api_id' in settings and len(settings['api_id']) > 0:
            self.settings = settings
        else:
            raise ValueError('api_id must well be defined on settings')

    def register(self, token, callback):
        """ Register a GCM device token validating it and
            generates a Device object.

            token: The device registration id.
            callback: the function to be executed when the registration completes
        """
        callback(Device(GCMPushService.type, token))

    def send(self, message, device_list, callback):
        """ Sends a message to a GCM device list, when the GCM server response executes
            the callback with the GCM response.

            message: The Message to be sent to the device list.
            device_list: A DeviceList with at least 1 GCM Device.
            callback: the function to be executed when the GCM response is received.
        """
        if(device_list.length() < 1):
            raise ValueError('DeviceList must contains at least 1 Device')
        callback(SendStatus(code=200, success=1, failure=0))
