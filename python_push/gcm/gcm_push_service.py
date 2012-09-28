from python_push.push_service import PushService
from python_push.device import Device
from python_push.send_status import SendStatus
import grequests
import json


class GCMPushService(PushService):
    """GCM Push Service implementation"""
    settings = None
    type = "GA"

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
            raise ValueError('device_list must contains at least 1 Device')

        # UNTESTED
        registration_ids = map(
            lambda device: device.token,
            filter(
                lambda device:
                    device.type == GCMPushService.type,
                device_list
            )
        )

        # UNTESTED
        body = {'registration_ids': registration_ids}
        # UNTESTED
        if(message.payload != None):
            body['data'] = message.payload
        # UNTESTED
        body_str = json.dumps(body)
        # UNTESTED
        headers = {
            'Content-Type': 'application/json',
            'Content-length': str(len(body_str.decode("utf-8"))),
            'Authorization': 'key=%s' % self.settings['api_id']
        }

        def response_cb(res):
            code = res.status_code
            assert isinstance(code, int)
            callback(
                SendStatus(
                    code=code,
                    success=res.json['success'] if code == 200 else None,
                    failure=res.json['failure'] if code == 200 else None,
                    raw=res.text
                )
            )

        # UNTESTED
        req = grequests.post(
            'https://android.googleapis.com/gcm/send',
            data=body_str,
            headers=headers,
            hooks={'response': response_cb}
        )
        req.send()
