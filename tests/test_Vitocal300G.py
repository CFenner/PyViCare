import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal300G(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal300G.json')
        self.device = HeatPump(self.service)

    def test_getCompressorActive(self):
        self.assertEqual(self.device.compressors[0].getActive(), False)

    def test_getCompressorHours(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHours(), 384.3)

    def test_getCompressorStarts(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getStarts(), 436)

    @unittest.skip("data point not present in the current test response")
    def test_getCompressorHoursLoadClass(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass1(), 30)
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass2(), 703)
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass3(), 878)
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass4(), 117)
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass5(), 20)

    def test_getHeatingCurveSlope(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveSlope(), 0.4)

    def test_getHeatingCurveShift(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveShift(), 0)

    def test_getReturnTemperature(self):
        self.assertAlmostEqual(self.device.getReturnTemperature(), 26.1)

    def test_getReturnTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(self.device.getReturnTemperaturePrimaryCircuit(), 28)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 28.8)

    def test_getPrograms(self):
        expected_programs = ['comfort', 'eco', 'fixed', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            expected_programs, self.device.circuits[0].getPrograms())

    def test_getModes(self):
        expected_modes = ['dhw', 'dhwAndHeating', 'standby']
        self.assertListEqual(
            expected_modes, self.device.circuits[0].getModes())

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), True)
