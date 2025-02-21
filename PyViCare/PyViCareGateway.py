from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleAPICommandErrors, handleNotSupported


class Gateway(Device):

    @handleNotSupported
    def getSerial(self):
        return self.service.getProperty("gateway.devices")["gatewayId"]

    @handleNotSupported
    def getWifiSignalStrength(self):
        return self.service.getProperty("gateway.wifi")["properties"]["strength"]["value"]

    @handleAPICommandErrors
    def reboot(self):
        return self.service.executeEquipmentAction("reboot")
