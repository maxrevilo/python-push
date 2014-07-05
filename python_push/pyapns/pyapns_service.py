import re
import copy
# import os.path
from python_push.utils import deep_update
from python_push.push_service import PushService
from python_push.push_response import PushResponse
from pyapns_request import PyAPNSRequest


# UNTESTED
class PyAPNSService(PushService):
    """PyAPNS Service implementation"""
    settings = None
    # Google Android
    type = 'AI'

    # TODO: Don't assume Django provissioning
    def __init__(self, settings):
        """ Initializes the PyAPNS Push Service with the specified settings.
            settings: {
                cert_file: The Path to the key certificate file with .pem extension.

                defaults: The options applied as the 'aps' dictionary.
                {
                    app_id: 'default',
                    alert: {
                        'body': None,
                        'action-loc-key': None,
                        'loc-key': None,
                        'loc-args': None,
                        'launch-image': None,
                    },
                    payload: {},
                    bagde: 1,
                    sound: 'default',
                    content-available: 0
                }
            }
        """
        self.settings = {
            'cert_file': None,
            'app_id': 'default',
            'defaults': {
                'alert': {
                    'body': None,
                    'action-loc-key': None,
                    'loc-key': None,
                    'loc-args': None,
                    'launch-image': None,
                },
                'payload': {},
                'bagde': 1,
                'sound': None,
                'content-available': 0
            }
        }

        if 'cert_file' in settings and len(settings['cert_file']) > 0:
            # if not os.path.isfile(settings['cert_file']):
            #     raise 'Certificate file not found on path "{}"'.format(settings['cert_file'])
            deep_update(settings, self.settings)
        else:
            raise ValueError('cert_file must be defined on settings')

    def send_request(self, message, device_list):
        """ Return the request for Send a message to the PyAPNSs devices on the list.

            message: The Message to be sent to the device list.
            device_list: A DeviceList with at least 1 PyAPNS Device.
        """

        token_cleaner = re.compile('[<> ]')
        tokens = map(
            lambda device: token_cleaner.sub('', device.token),
            filter(
                lambda device:
                    device.type == PyAPNSService.type,
                device_list
            )
        )

        if(len(tokens) < 1):
            raise ValueError('device_list must contains at least 1 PyAPNS Device')

        notification = {'aps': None}
        notification['aps'] = copy.deepcopy(self.settings['defaults'])

        if message.options is not None:
            deep_update(message.options, notification['aps'])

        if message.payload is not None:
            deep_update(message.payload, notification['aps']['payload'])

        def response_builder(res):
            code = res.status
            return PushResponse(
                type=PyAPNSService.type,
                code=code,
                is_ok=code == 200,
                raw=res.text
            )

        return PyAPNSRequest(
            type=PyAPNSService.type,
            app_id=self.settings['app_id'],
            url=None,
            tokens=tokens,
            notification=notification,
            response_builder=response_builder
        )
