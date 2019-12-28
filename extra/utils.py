ERROR_WIFI = 0, "WIFI"
ERROR_NTC = 1, "NTC"
ERROR_LOOP = 2, "LOOP"
ERROR_MEM = 3, "MEM"
ERROR_SRV = 4, "SRV"


def arduino_map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def iso8601(time):
    val = b"{0}-{1}-{2} {3}:{4}"
    return val.format(*time)


_screen_cache = {}


def update_screen(l1="", l2=""):
    try:
        import machine, utime, ssd1306
        if "i2c" not in _screen_cache:
            _screen_cache["i2c"] = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
        if "ssd" not in _screen_cache:
            _screen_cache["ssd"] = ssd1306.SSD1306_I2C(128, 32, _screen_cache["i2c"])
        _screen_cache["ssd"].fill(0)
        _screen_cache["ssd"].text(l1, 0, 0)
        _screen_cache["ssd"].text(l2, 0, 16)
        _screen_cache["ssd"].show()
    except:
        pass


def error_leds(status):
    import machine, time
    red = machine.Pin(0, machine.Pin.OUT)
    red.value(1)

    if status == ERROR_WIFI:
        red.value(0)
        time.sleep(0.1)
        red.value(1)
    elif status == ERROR_NTC:
        red.value(0)
        time.sleep(0.1)
        red.value(1)
        time.sleep(0.1)
        red.value(0)
        time.sleep(0.1)
        red.value(1)
    elif status == ERROR_LOOP:
        red.value(0)
        time.sleep(0.3)
        red.value(1)
        time.sleep(0.1)
        red.value(0)
        time.sleep(0.1)
        red.value(1)
    elif status == ERROR_MEM:
        red.value(0)
        time.sleep(0.3)
        red.value(1)
        time.sleep(0.1)
        red.value(0)
        time.sleep(0.3)
        red.value(1)
    elif status == ERROR_SRV:
        red.value(0)
        time.sleep(0.1)
        red.value(1)
        time.sleep(0.1)
        red.value(0)
        time.sleep(0.3)
        red.value(1)

    update_screen("ERROR: {}".format(status[1]))

