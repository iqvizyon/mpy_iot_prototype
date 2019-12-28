def do_connect():
    import network, ujson
    with open("/data/wifi.json") as f:
        known = ujson.loads(f.read())
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    scanned = [x[0].decode() for x in wlan.scan() if x[0].decode() in known]
    for ssid in scanned:
        wlan.connect(ssid, known[ssid])
        while wlan.status() == network.STAT_CONNECTING:
            pass
        if wlan.status() != network.STAT_GOT_IP:
            continue
        else:
            return wlan.ifconfig()[0]
    else:
        raise OSError("Can't Connect")
