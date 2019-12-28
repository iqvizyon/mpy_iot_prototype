import machine, utime, micropython, ujson

from extra.utils import error_leds, ERROR_SRV
from lib import urequests


class Client:
    def __init__(self, endpoint, token):
        self._token = token
        self._endpoint = endpoint

    def process(self, sensor):
        try:
            urequests.post(url="{}/iot/api/in/".format(self._endpoint),
                           data=sensor.serialized_data(),
                           headers={"Authorization": "Token {}".format(self._token),
                                    "Content-Type": "application/json"})
        except Exception as e:
            from extra.utils import update_screen
            error_leds(ERROR_SRV)
            raise e
