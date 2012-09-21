import unittest
from ..gcm_push_service import GCMPushService
from python_push.send_status import SendStatus
from python_push.message import Message
from python_push.device import Device
#from time import sleep


TOKEN = 'GENERIC_DEVICE_TOKEN'
API_ID = 'AIzaSyCwR74jMF8Ls0CXvJzKHMpHVQzwml9xmTI'


class TestGCMPushService(unittest.TestCase):

    def test_init_settings_must_have_api_id(self):
        self.assertRaises(ValueError, GCMPushService, {})
        self.assertRaises(ValueError, GCMPushService, {'asd': ''})
        self.assertRaises(ValueError, GCMPushService, {'api_id': ''})
        # This should run without problems
        GCMPushService({'api_id': API_ID})

    def test_register_generates_device(self):
        gcm_srv = GCMPushService({'api_id': API_ID})

        global callback_called
        callback_called = False

        def callback_test(device):
            global callback_called
            callback_called = True
            #self.assertIsInstance(device, Device)
            self.assertTrue(device.type == GCMPushService.type)
            self.assertTrue(device.token == TOKEN)

        gcm_srv.register(TOKEN, callback_test)

        #This will be necesary if gcm_srv.register connect to GCM.
        #if not callback_called:
        #    sleep(.001)

        self.assertTrue(callback_called)

    def test_send_collapsible_message(self):
        msg = Message()
        msg.set_option('collapse_key', 'test')

        gcm_srv = GCMPushService({'api_id': API_ID})

        global register_callback_called
        register_callback_called = False

        def register_callback(device):
            global send_callback_called
            send_callback_called = False

            device_list = [device]

            def send_callback(send_status):
                self.assertIsInstance(send_status, SendStatus)
                self.assertTrue(send_status.code in [200, 400, 401, 500, 503])
                if(send_status.code == 200):
                    self.assertTrue(
                        send_status.success ==
                            len(device_list) - send_status.failure
                    )
                #self.assertTrue(send_status.canonical_ids == 0)

                global send_callback_called
                send_callback_called = True

            gcm_srv.send(msg, device_list, send_callback)
            self.assertTrue(send_callback_called)

            global register_callback_called
            register_callback_called = True

        gcm_srv.register(TOKEN, register_callback)
        self.assertTrue(register_callback_called)

    def test_send_message_device_list_have_at_least_one_device(self):
        msg = Message()
        gcm_srv = GCMPushService({'api_id': API_ID})

        device_list = []

        global send_callback_called
        send_callback_called = False

        def send_callback(send_status):

            global send_callback_called
            send_callback_called = True

        self.assertRaises(ValueError, gcm_srv.send,
            msg, device_list, send_callback
        )

        device_list.append(Device(token=None, type=None))
        # This should run without problems
        gcm_srv.send(msg, device_list, send_callback)
        self.assertTrue(send_callback_called)


if __name__ == '__main__':
    unittest.main()
