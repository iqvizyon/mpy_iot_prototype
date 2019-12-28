from lib import lis3dh
from sensors.base import BaseSensor


class Sensor(BaseSensor):

    def __init__(self, i2c, address=None, *args, **kwargs):
        _dr_ar = [i2c]
        if address is not None:
            _dr_ar.append(address)
        self._driver = lis3dh.LIS3DH_I2C(*_dr_ar)
        super().__init__(*args, **kwargs)

    def read_second(self):
        if self._current_data:
            return max(self._current_data) - min(self._current_data)  # max vibration

    def read_data(self):
        return int(sum([x / 9.806 for x in self._driver.acceleration]) * 100)  # total cm/s^2
