import unittest
from ..gcm_push_service import GCMPushService


class TestGCMPushServiceRegister(unittest.TestCase):

    def test_init_settings_must_have_api_id(self):
        self.assertRaises(ValueError, GCMPushService, {})
        self.assertRaises(ValueError, GCMPushService, {'asd': ''})
        self.assertRaises(ValueError, GCMPushService, {'api_id': ''})


if __name__ == '__main__':
    unittest.main()
