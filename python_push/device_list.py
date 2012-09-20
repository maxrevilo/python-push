from python_push.device import Device


class DeviceList:
    """Hold a list of Devices"""
    _devices = None

    def __init__(self):
        self._devices = []

    def __iter__(self):
        for d in self._devices:
            yield d

    def add(self, device):
        assert device not in self._devices
        assert isinstance(device, Device)

        self._devices.append(device)

    def length(self):
        return len(self._devices)
