import unittest
from ..bb_push_service import BBPushService
from python_push.push_response import PushResponse
from python_push.message import Message
from python_push.device import Device


TOKEN = 'PIN00001'
API_ID = '2974-Mie72996c2B7m3t87M17o8172i80r505273'
PASSWORD = 'dsvoolM5'


class TestBBPushService(unittest.TestCase):

    def test_init_settings_must_have_api_id(self):
        self.assertRaises(ValueError, BBPushService, {})
        self.assertRaises(ValueError, BBPushService, {'asd': ''})
        self.assertRaises(ValueError, BBPushService, {'api_id': '', 'password': ''})
        # This should run without problems
        BBPushService({'api_id': API_ID, 'password': PASSWORD})

    def test_send_message_no_expiration_date(self):
        msg = Message()
        gcm_srv = BBPushService({'api_id': API_ID, 'password': PASSWORD})
        device_list = [Device(BBPushService.type, TOKEN)]

        push_response = gcm_srv.send(msg, device_list)

        self.assertIsInstance(push_response, PushResponse)
        self.assertTrue(push_response.code in (1000, 1001, 2001, 2002, 2004, 4001, 21000),
            '\nStatus Code %i:\n%s\n' % (push_response.code, push_response.description)
        )

if __name__ == '__main__':
    unittest.main()
