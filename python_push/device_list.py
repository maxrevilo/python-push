class DeviceList:
    """Hold a list of Devices"""
    _devices = []

    def __init__(self):
        pass

    def add(self, device):
        self._devices.append(device)
