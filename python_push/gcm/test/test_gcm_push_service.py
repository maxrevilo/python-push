import unittest
from ..gcm_push_service import GCMPushService
from python_push.device import Device
from python_push.device_list import DeviceList
from python_push.send_status import SendStatus
from python_push.message import Message
#from time import sleep


class TestGCMPushServiceRegister(unittest.TestCase):

    def test_init_settings_must_have_api_id(self):
        self.assertRaises(ValueError, GCMPushService, {})
        self.assertRaises(ValueError, GCMPushService, {'asd': ''})
        self.assertRaises(ValueError, GCMPushService, {'api_id': ''})

    def test_register_generates_device__i__(self):
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

    def test_send_collapsible_message__i__(self):
        token = 'GENERIC_DEVICE_TOKEN'

        msg = Message()
        msg.set_option('collapse_key', 'test')

        gcm_srv = GCMPushService({'api_id': 'GENERIC_API_ID'})

        global register_callback_called
        register_callback_called = False

        def register_callback(device):
            global send_callback_called
            send_callback_called = False

            device_list = DeviceList()
            device_list.add(device)

            def send_callback(send_status):
                self.assertIsInstance(send_status, SendStatus)
                self.assertTrue(send_status.code == 200)
                self.assertTrue(send_status.success == 1)
                self.assertTrue(send_status.failure == 0)
                #self.assertTrue(send_status.canonical_ids == 0)

                global send_callback_called
                send_callback_called = True

            gcm_srv.send(msg, device_list, send_callback)
            self.assertTrue(send_callback_called)

            global register_callback_called
            register_callback_called = True

        gcm_srv.register(token, register_callback)
        self.assertTrue(register_callback_called)

if __name__ == '__main__':
    unittest.main()
