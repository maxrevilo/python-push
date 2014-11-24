import re
import copy
import json
# import os.path
from asynchttp import Http
from python_push.utils import deep_update
from python_push.push_service import PushService
from python_push.push_response import PushResponse
from python_push.push_request import PushRequest


# UNTESTED
class ParseAIService(PushService):
    """ParseAI Service implementation"""
    settings = None
    # Apple iOS
    type = 'AI'
    url = 'https://api.parse.com/1/'

    # TODO: Don't assume Django provissioning
    def __init__(self, settings):
        """ Initializes the ParseAI Push Service with the specified settings.
            settings: {
                app_id: Application ID on Parse.
                rest_key: REST API Key for Parse.

                defaults: The options applied as the 'aps' dictionary.
                {
                    'alert': 'Alert',
                    'badge': 1,
                    'sound': None,
                    'content-available': 0,
                    'category': None
                }
            }
        """
        self.settings = {
            'app_id': None,
            'rest_key': None,
            'defaults': {
                'alert': 'Alert',
                'badge': 1,
                'sound': None,
                'content-available': 0,
                'category': None,
                'payload': {},
            }
        }

        if 'app_id' not in settings or len(settings['app_id']) == 0:
            raise ValueError('app_id must be defined on settings')
        if 'rest_key' not in settings or len(settings['rest_key']) == 0:
            raise ValueError('rest_key must be defined on settings')

        deep_update(settings, self.settings)

    def send_request(self, message, device_list):
        """ Return the request for Send a message to the ParseAIs devices on the list.

            message: The Message to be sent to the device list.
            device_list: A DeviceList with at least 1 ParseAI Device.
        """

        token_cleaner = re.compile('[<> ]')
        tokens = map(
            lambda device: token_cleaner.sub('', device.token),
            filter(
                lambda device:
                    device.type == ParseAIService.type,
                device_list
            )
        )

        if(len(tokens) < 1):
            raise ValueError('device_list must contains at least 1 Apple Device')

        notification = copy.deepcopy(self.settings['defaults'])

        if message.options is not None:
            deep_update(message.options, notification)

        if message.payload is not None:
            deep_update(message.payload, notification['payload'])

        headers = {
            'Content-Type': 'application/json',
            'X-Parse-Application-Id': self.settings['app_id'],
            'X-Parse-REST-API-Key': self.settings['rest_key']
        }

        def response_builder(res):
            code = res.status
            if code == 200:
                try:
                    json_resp = json.loads(res.text)
                except ValueError:
                    raise ValueError("Response from Parse Server is not JSON formated")
            else:
                json_resp = {}

            return PushResponse(
                type=ParseAIService.type,
                code=code,
                is_ok=json_resp.get("result"),
                raw=res.text
            )

        # We must register all devices before send the push:
        self._register_installations(headers, tokens)

        return PushRequest(
            type=ParseAIService.type,
            url=self.url + 'push',
            headers=headers,
            body=json.dumps({
                "channels": ["device-ai-"+token for token in tokens],
                "data": notification
            }),
            response_builder=response_builder,
            ssl_certificate_validation=False
        )

    def _register_installations(self, headers, tokens):
        promises = []
        url = self.url + 'installations'
        for token in tokens:
            response_promise, _ = Http(disable_ssl_certificate_validation=True).request(
                uri=url,
                method="POST",
                body=json.dumps({
                    "deviceType": "ios",
                    "deviceToken": token,
                    "channels": ["device-ai-"+token]
                }),
                headers=headers,
            )
            promises.append(response_promise)

        for promise in promises:
            promise.wait()
