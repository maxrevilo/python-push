import unittest

from python_push.push_manager import PushManager
from python_push.gcm.gcm_push_service import GCMPushService
from python_push.blackberry.bb_push_service import BBPushService


BLACKBERRY_OPS = {
    'api_id': '2974-Mie72996c2B7m3t87M17o8172i80r505273',
    'password': 'dsvoolM5'
}

GCM_OPS = {
    'api_id': 'AIzaSyCwR74jMF8Ls0CXvJzKHMpHVQzwml9xmTI'
}


class TestMessage(unittest.TestCase):

    def test_push_manager_init_with_all_services(self):
        pm = PushManager([
            GCMPushService(GCM_OPS),
            BBPushService(BLACKBERRY_OPS)
        ])

        self.assertTrue(pm.get_service(GCMPushService.type))
        self.assertTrue(pm.get_service(BBPushService.type))

        self.assertTrue(pm.get_service('Must NOT exist') == None)

    def test_push_manager_add_push_service(self):
        pass  # pm = PushManager()
