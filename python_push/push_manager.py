from python_push.push_service import PushService


class PushManager:
    """ Manager for send Push Notification to a list of
        Push Services"""

    _services = None

    def __init__(self, push_services=[]):
        self._services = push_services

    def add_service(self, push_service):
        """ Add a PushService to the services list."""
        assert isinstance(push_service, PushService)
        self._services.append(push_service)

    def get_service(self, push_service_type):
        """ Retrieve a PushService from the services list."""
        for push_service in self._services:
            if push_service.type == push_service_type:
                return push_service
        return None

    def send(self, message, device_list):
        """ Send a message to a devices list using all the PushServices
            on the services list.
        """
        status_dict = {}
        push_requests = []

        for push_service in self._services:
            try:
                req = push_service.send_request(message, device_list).send()
                push_requests.append(req)
            except ValueError:
                pass

        for req in push_requests:
            #req.push_response blocks until get the response
            status_dict[req.type] = req.push_response

        return status_dict
