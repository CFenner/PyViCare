from PyViCare.PyViCareHeatingDevice import HeatingDevice


class HeatingDeviceWithComponent:
    """This is the base class for all heating components"""

    def __init__(self, device: HeatingDevice, component: str) -> None:
        self.service = device.service
        self.component = component
        self.device = device

    @property
    def id(self) -> str:
        return self.component
