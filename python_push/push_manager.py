class PushManager:
    """ Manager for send Push Notification to a list of
        Push Services"""

    _services = None

    def __init__(self, push_services=[]):
        self._services = push_services

    def add_service(push_service_type):
        pass

    def get_service(self, push_service_type):
        for push_service in self._services:
            if push_service.type == push_service_type:
                return push_service
        return None
