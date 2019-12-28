from extra.utils import arduino_map
from sensors.base import BaseSensor


class Sensor(BaseSensor):
    def __init__(self, adc, *args, **kwargs):
        self._driver = adc
        super().__init__(*args, **kwargs)

    def read_second(self):
        if self._current_data:
            return max(self._current_data) - min(self._current_data)  # max noise

    def read_data(self):
        return arduino_map(self._driver.read(), 0, 1024, 0, 100)  # no unit
