import gc
import micropython
import sys
import utime
import network

from extra.utils import error_leds, ERROR_LOOP, ERROR_MEM, ERROR_WIFI, ERROR_NTC, update_screen, iso8601

wlan = network.WLAN(network.STA_IF)
_errors = False

def main():
    try:
        from extra.wifi import do_connect

        do_connect()
        update_screen("Connected", wlan.ifconfig()[0])
    except (SyntaxError, OSError, ValueError, LookupError, ArithmeticError, NameError) as e:
        print(micropython.mem_info(1))
        sys.print_exception(e)
        error_leds(ERROR_WIFI)
        raise e
    finally:
        gc.collect()

    try:
        from ntp import settime

        settime()
        update_screen("Updated Time", iso8601(utime.localtime()))
    except (SyntaxError, OSError, ValueError, LookupError, ArithmeticError, NameError) as e:
        print(micropython.mem_info(1))
        sys.print_exception(e)
        error_leds(ERROR_NTC)
        raise e
    finally:
        gc.collect()

    try:
        from extra import mainloop

        mainloop.loop()
    except MemoryError as e:
        print(micropython.mem_info(1))
        sys.print_exception(e)
        error_leds(ERROR_MEM)
    except (SyntaxError, OSError, ValueError, LookupError, ArithmeticError, NameError) as e:
        print(micropython.mem_info(1))
        sys.print_exception(e)
        error_leds(ERROR_LOOP)
        raise e
    finally:
        gc.collect()

main()