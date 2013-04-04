from random import random
from datetime import datetime, timedelta
import base64
import re

from python_push.push_service import PushService
from python_push.utils import now_epoch, date2utc
from python_push.push_request import PushRequest
from python_push.push_response import PushResponse


BOUNDARY = "8d5588928a90afd3009d"


class BBPushService(PushService):
    """Blackberry Push Service implementation"""
    settings = None
    type = "BO"

    def __init__(self, settings):
        """ Initializes the Blackberry Push Service with the specified settings.
            settings: {
                api_id: Blackberry App Key.
                password: Blackberry App Password

                defaults: The options applied to an push if they are not specified.
                {
                    ...
                }
            }
        """
        if not 'api_id' in settings or len(settings['api_id']) == 0:
            raise ValueError('api_id must well be defined on settings')
        elif not 'password' in settings or len(settings['api_id']) == 0:
            raise ValueError('password must well be defined on settings')
        else:
            self.settings = settings

    def send_request(self, message, device_list):
        """ Return the request for Send a message to a Blackberry device list.

            message: The Message to be sent to the device list.
            device_list: A DeviceList with at least 1 Blackberry Device.
        """
        # UNTESTED
        registration_ids = reduce(
            lambda xml, device:
                xml + '<address address-value="%s"/>' % device.token
                    if device.type == BBPushService.type
                else xml,
            device_list,
            ''
        )

        if(registration_ids == ''):
            raise ValueError('device_list must contains at least 1 Blackberry Device')

        # UNTESTED
        push_id = str(round(now_epoch() * random() + now_epoch()))
        exp_date = date2utc(datetime.now() + timedelta(days=30))
        data = 'PING'
        request_body = "--" + BOUNDARY + "\n" +\
            'Content-Type: application/xml; charset=UTF-8\n' +\
            '\n' +\
            '<?xml version="1.0"?>\n' +\
            '<!DOCTYPE pap PUBLIC "-//WAPFORUM//DTD PAP 2.1//EN" ' +\
                                    '"http://www.openmobilealliance.org/tech/DTD/pap_2.1.dtd">\n' +\
            '<pap>\n' +\
            '  <push-message push-id="' + push_id + '" deliver-before-timestamp="' +\
                                    exp_date + '" source-reference="' + self.settings['api_id'] + '">\n' +\
            '  ' + registration_ids + "\n" +\
            '  <quality-of-service delivery-method="unconfirmed"/>\n' +\
            '  </push-message>\n' +\
            '</pap>\n' +\
            '--' + BOUNDARY + '\n' +\
            'Content-Type: text/plain\n' +\
            '\n' +\
            data + '\n' +\
            '--' + BOUNDARY + '--'

        # UNTESTED
        headers = {
            "User-Agent": "Python Push Library",
            "Authorization": "Basic %s" % base64.b64encode(b'%s:%s' % (self.settings['api_id'], self.settings['password'])),
            "Content-Type": "multipart/related; boundary=%s; type=application/xml" % BOUNDARY,
            'Content-length': str(len(request_body.decode("utf-8"))),
        }

        def response_builder(res):
            code = res.status
            assert isinstance(code, int)
            if(code == 200):
                #The easiest way is use regex due to Server non-standard responses
                #This is the status code sent by BlackBerry Server:
                bb_code = int(re.search(r'code=\"(.+?)\"', res.text).groups()[0])
                bb_desc = re.search(r'desc=\"(.+?)\"', res.text).groups()[0]
                return PushResponse(
                    type=BBPushService.type,
                    code=bb_code,
                    is_ok=bb_code in (1000, 1001),
                    description=bb_desc,
                    raw=res.text
                )
            else:
                raise Exception("Error connecting with Blackberry server")

        # UNTESTED
        return PushRequest(
            type=BBPushService.type,
            url='https://cp2974.pushapi.eval.blackberry.com:443/mss/PD_pushRequest',
            headers=headers,
            body=request_body,
            response_builder=response_builder
        )

    # def send(self, message, device_list):
    #     """ Sends a message to a Blackberry device list and returns the Response.

    #         message: The Message to be sent to the device list.
    #         device_list: A DeviceList with at least 1 Blackberry Device.
    #     """
    #     return self.send_request(message, device_list).send().wait()
