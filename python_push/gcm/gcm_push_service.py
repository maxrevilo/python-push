from python_push.push_service import PushService
from python_push.push_response import PushResponse
from python_push.push_request import PushRequest
import grequests
import json


class GCMPushService(PushService):
    """GCM Push Service implementation"""
    settings = None
    # Google Android
    type = 'GA'

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

    def send_request(self, message, device_list):
        """ Return the request for Send a message to a GCM device list.

            message: The Message to be sent to the device list.
            device_list: A DeviceList with at least 1 GCM Device.
        """
        # UNTESTED
        registration_ids = map(
            lambda device: device.token,
            filter(
                lambda device:
                    device.type == GCMPushService.type,
                device_list
            )
        )

        if(len(registration_ids) < 1):
            raise ValueError('device_list must contains at least GCM 1 Device')

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

        def response_builder(res):
            code = res.status_code
            assert isinstance(code, int)
            return PushResponse(
                    type=GCMPushService.type,
                    code=code,
                    is_ok=code == 200,
                    success=res.json['success'] if code == 200 else None,
                    failure=res.json['failure'] if code == 200 else None,
                    raw=res.text
                )

        # UNTESTED
        return PushRequest(
            type=GCMPushService.type,
            request=grequests.post(
                'https://android.googleapis.com/gcm/send',
                data=body_str,
                headers=headers
            ),
            response_builder=response_builder
        )

    def send(self, message, device_list):
        """ Sends a message to a GCM device list and returns the Response.

            message: The Message to be sent to the device list.
            device_list: A DeviceList with at least 1 GCM Device.
        """
        return self.send_request(message, device_list).send()
