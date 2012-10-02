import unittest
from ..gcm_push_service import GCMPushService
from python_push.push_response import PushResponse
from python_push.message import Message
from python_push.device import Device


TOKEN = 'GENERIC_DEVICE_TOKEN'
API_ID = 'AIzaSyCwR74jMF8Ls0CXvJzKHMpHVQzwml9xmTI'


class TestGCMPushService(unittest.TestCase):

    def test_init_settings_must_have_api_id(self):
        self.assertRaises(ValueError, GCMPushService, {})
        self.assertRaises(ValueError, GCMPushService, {'asd': ''})
        self.assertRaises(ValueError, GCMPushService, {'api_id': ''})
        # This should run without problems
        GCMPushService({'api_id': API_ID})

    def test_send_collapsible_message(self):
        msg = Message()
        msg.set_option('collapse_key', 'test')

        gcm_srv = GCMPushService({'api_id': API_ID})
        device_list = [Device(GCMPushService.type, TOKEN)]

        push_response = gcm_srv.send(msg, device_list)

        self.assertIsInstance(push_response, PushResponse)
        self.assertTrue(push_response.code in (200, 503))
        if(push_response.code == 200):
            self.assertTrue(
                push_response.success ==
                    len(device_list) - push_response.failure
            )

    def test_send_message_device_list_have_at_least_one_device(self):
        msg = Message()
        gcm_srv = GCMPushService({'api_id': API_ID})
        device_list = []

        self.assertRaises(ValueError, gcm_srv.send, msg, device_list)

        device_list.append(Device(token=None, type=None))
        # This should run without problems
        gcm_srv.send(msg, device_list)


if __name__ == '__main__':
    unittest.main()
