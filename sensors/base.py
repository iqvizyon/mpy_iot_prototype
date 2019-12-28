import utime, ujson

from extra.utils import iso8601


class BaseSensor:
    default_value = None

    def __init__(self, name=None):
        self._name = name
        self._raw = [self.default_value] * 60
        self._time_cursor = utime.localtime()[:6]
        self._last_time_cursor = utime.localtime()[:6]
        self._current_data = []

    def read_data(self):
        raise NotImplementedError

    def read_second(self):
        raise NotImplementedError

    def update_second(self):
        self._current_data.append(self.read_data())

    def update_minute(self, second):
        sec = self.read_second()
        if sec is not None:
            self._raw[second] = sec
        self._current_data = []

    def clean_data(self):
        for i in range(len(self._raw)):
            self._raw[i] = self.default_value

    def time_cursor_iso8601(self, time=None):
        if time is None:
            time = self._time_cursor
        return iso8601(time)

    def serialized_data(self):
        val = ujson.dumps({
            b"raw": self._raw,
            b"time": self.time_cursor_iso8601(self._last_time_cursor),
            b"source_id": self._name
        })
        self.clean_data()
        return val

    def update(self, now):
        res = False
        if self._time_cursor == now:  # same second
            self.update_second()
        elif self._time_cursor[:5] == now[:5]:  # same minute
            self.update_minute(now[-1])
        else:
            self.update_minute(now[-1])
            self._last_time_cursor = self._time_cursor
            res = True
        self._time_cursor = now[:6]
        return res
