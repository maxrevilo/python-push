import time
import logging
import pyapns.client
from python_push.push_request import PushRequest
from python_push.push_response import PushResponse


class PyAPNSRequest(PushRequest):
    """Represents an PyAPNS Service request for send a push to the Apple Push Service"""
    type = None
    url = None
    app_id = None
    notification = None

    response_builder = None
    _push_response = None

    def __init__(self, type, app_id, url, tokens, notification, response_builder):
        """ Creates an XML-RPC Request to the PyAPNS Server.
        """
        self.type = type
        self.app_id = app_id
        self.url = url
        self.tokens = tokens
        self.notification = notification
        self.response_builder = response_builder
        #Default response:
        self._push_response = PushResponse(type=self.type, code=0, is_ok=False, raw='Not sended')

    def send(self):
        """ Sends this PushRequest to the PyAPNS server and returns the PushResponse"""
        for token in self.tokens:
            """
                We send tokens one by one to avoid the probem of the n-1th token:
                http://stackoverflow.com/questions/1759101/multiple-iphone-apn-messages-single-connection
            """
            self._notify(self.app_id, [token], [self.notification])
        self._push_response = PushResponse(type=self.type, code=200, is_ok=True, raw='Sended without response.')
        return self

    def wait(self):
        """ After being sended wait until get the response. """
        #TODO: If the wait is optional this can wait to the feedback response.
        return self

    @property
    def push_response(self):
        return self._push_response

    def _notify(self, app_id, tokens, notifications):
        """
        Credits to http://kbyanc.blogspot.com/2010/09/using-pyapns-with-django.html
        """
        log = logging.getLogger('APNS')

        for attempt in range(4):
            try:
                print notifications
                pyapns.client.notify(app_id, tokens, notifications)
                break
            except (pyapns.client.UnknownAppID,
                    pyapns.client.APNSNotConfigured):
                # This can happen if the pyapns server has been
                # restarted since django started running.  In
                # that case, we need to clear the client's
                # configured flag so we can reconfigure it from
                # our settings.py PYAPNS_CONFIG settings.
                if attempt == 3:
                    log.exception()
                pyapns.client.OPTIONS['CONFIGURED'] = False
                pyapns.client.configure({})
                time.sleep(0.5)
