from python_push.push_service import PushService


class PushManager:
    """ Manager for send Push Notification to a list of
        Push Services"""

    _services = None

    def __init__(self, push_services=[]):
        self._services = push_services

    def add_service(self, push_service):
        assert isinstance(push_service, PushService)
        self._services.append(push_service)

    def get_service(self, push_service_type):
        for push_service in self._services:
            if push_service.type == push_service_type:
                return push_service
        return None

    def send(self, message, device_list):
        status_dict = {}

        def dummy(st):
            status_dict['XX'] = st

        for push_service in self._services:
            clean_list = []
            for device in device_list:
                if(device.type == push_service.type):
                    clean_list.append(device)
            push_service.send(message, device, callback)
