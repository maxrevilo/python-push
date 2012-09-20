import unittest
from python_push.message import Message


class TestMessage(unittest.TestCase):

    def test_message_set_option(self):
        msg = Message()
        msg.set_option('key', 'value')
        self.assertTrue('key' in msg.options)
        self.assertTrue(msg.options['key'] == 'value')
