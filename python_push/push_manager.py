from python_push.push_service import PushService
import grequests


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
        python_requests = []

        for push_service in self._services:
            try:
                pr = push_service.send_request(message, device_list)
                push_requests.append(pr)
                python_requests.append(pr._request)
            except ValueError:
                pass

        grequests.map(python_requests)

        for pr in push_requests:
            status_dict[pr.type] = pr.push_response

        return status_dict
