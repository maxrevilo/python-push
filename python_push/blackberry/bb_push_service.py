from python_push.push_service import PushService

BOUNDARY = "8d5588928a90afd3009d"


class BBPushService(PushService):
    """Blackberry Push Service implementation"""
    settings = None
    type = "BO"

    def __init__(self, settings):
        """ Initializes the Blackberry Push Service with the specified settings.
            settings: {
                api_id: Blackberry App Key.
                password: Blackberry App Password

                defaults: The options applied to an push if they are not specified.
                {
                    ...
                }
            }
        """
        if not 'api_id' in settings or len(settings['api_id']) == 0:
            raise ValueError('api_id must well be defined on settings')
        elif not 'password' in settings or len(settings['api_id']) == 0:
            raise ValueError('password must well be defined on settings')
        else:
            self.settings = settings
