class DeviceList:
    """Hold a list of Devices"""
    _devices = None

    def __init__(self):
        self._devices = []

    def add(self, device):
        self._devices.append(device)

    def length(self):
        return len(self._devices)
