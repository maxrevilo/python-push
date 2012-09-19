import unittest
from ..gcm_push_service import GCMPushService
from python_push.device import Device
#from time import sleep


class TestGCMPushServiceRegister(unittest.TestCase):

    def test_init_settings_must_have_api_id(self):
        self.assertRaises(ValueError, GCMPushService, {})
        self.assertRaises(ValueError, GCMPushService, {'asd': ''})
        self.assertRaises(ValueError, GCMPushService, {'api_id': ''})

    def test_register_generates_device(self):
        gcm_srv = GCMPushService({'api_id': 'GENERIC_API_ID'})

        global callback_called
        callback_called = False
        token = 'GENERIC_DEVICE_TOKEN'

        def callback_test(device):
            global callback_called
            callback_called = True
            self.assertIsInstance(device, Device)
            self.assertTrue(device.type == GCMPushService.type)
            self.assertTrue(device.token == token)

        gcm_srv.register(token, callback_test)

        #This will be necesary if gcm_srv.register connect to GCM.
        #if not callback_called:
        #    sleep(.001)

        self.assertTrue(callback_called)

if __name__ == '__main__':
    unittest.main()
