import utime
import gc
import machine
import ubinascii
import ssd1306
import network
from extra import api
from extra.utils import iso8601, update_screen
from sensors import lis3dh, mic, sht31, tmp007

wlan = network.WLAN(network.STA_IF)
uid = ubinascii.hexlify(machine.unique_id()).decode()
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))


def _read_settings(uid):
    import ujson
    with open("/data/settings_{}.json".format(uid)) as f:
        return ujson.loads(f.read())


def _prepare():
    settings_json = _read_settings(uid)
    sensor_list = [
        lis3dh.Sensor(i2c, name=settings_json["lis3dh"]),
        mic.Sensor(machine.ADC(0), name=settings_json["mic"]),
        sht31.TempSensor(i2c, name=settings_json["sht31-temp"]),
        sht31.HumiSensor(i2c, name=settings_json["sht31-humi"]),
    ]
    client = api.Client(settings_json["server"], settings_json["token"])
    return sensor_list, client


def loop():
    sensor_list, client = _prepare()
    previous_now = utime.localtime()[:6]
    while True:
        now = utime.localtime()[:6]

        if previous_now[4] != now:
            update_screen(wlan.ifconfig()[0], iso8601(utime.localtime()))
            previous_now = now

        for s in sensor_list:
            if s.update(now):
                client.process(s)
            gc.collect()
        utime.sleep(0.1)
