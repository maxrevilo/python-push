import unittest
from ..bb_push_service import BBPushService


TOKEN = 'GENERIC_DEVICE_TOKEN'
API_ID = '2974-Mie72996c2B7m3t87M17o8172i80r505273'
PASSWORD = 'dsvoolM5'


class TestGCMPushService(unittest.TestCase):

    def test_init_settings_must_have_api_id(self):
        self.assertRaises(ValueError, BBPushService, {})
        self.assertRaises(ValueError, BBPushService, {'asd': ''})
        self.assertRaises(ValueError, BBPushService, {'api_id': '', 'password': ''})
        # This should run without problems
        BBPushService({'api_id': API_ID, 'password': PASSWORD})

if __name__ == '__main__':
    unittest.main()
