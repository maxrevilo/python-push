from python_push.push_service import PushService


class GCMPushService(PushService):
    """GCM Push Service implementation"""
    settings = None

    def __init__(self, settings):
        """ Initializes de GCM Push Service with the specified setings.
            settings: {
                api_id: Google Server API Key.

                defaults: The options applied to an push if they are not specified.
                {
                    collapse_key: ...
                    delay_while_idle: ...
                    time_to_live: ...
                }
            }
        """
        if 'api_id' in settings and len(settings['api_id']) > 0:
            self.settings = settings
        else:
            raise ValueError

    def register(self, token, callback):
        """ Register a GCM device token validating it and
            generates a Device object.

            token: The device registration id.
            callback: the function to be executed when the registration completes
        """
        pass

    def send(self, message, device, callback):
        pass
