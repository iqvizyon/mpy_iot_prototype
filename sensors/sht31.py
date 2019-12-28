from lib import sht31
from sensors.base import BaseSensor


class Sensor(BaseSensor):
    _shared_state = {b'dr': None, b'dr_args': ()}

    def __init__(self, i2c, address=None, *args, **kwargs):
        if self._shared_state[b"dr"] is None or self._shared_state[b"dr_args"] != (i2c, args):
            self._driver = self._shared_state[b"dr"] = self._get_sensor(i2c, address)
            self._shared_state[b"dr_args"] = (i2c, args)
        else:
            self._driver = self._shared_state[b"dr"]
        super().__init__(*args, **kwargs)

    def _get_sensor(self, i2c, address=None):
        _dr_ar = [i2c]
        if address is not None:
            _dr_ar.append(address)
        return sht31.SHT31(*_dr_ar)

    def read_second(self):
        if self._current_data:
            return int(sum(self._current_data) / len(self._current_data))  # avg value


    def get_temp(self):
        return self._driver.get_temp_humi()[0]

    def get_humi(self):
        return self._driver.get_temp_humi()[1]

    def read_data(self):
        raise NotImplementedError


class TempSensor(Sensor):
    def read_data(self):
        return int(self.get_temp())


class HumiSensor(Sensor):
    def read_data(self):
        return int(self.get_humi())
