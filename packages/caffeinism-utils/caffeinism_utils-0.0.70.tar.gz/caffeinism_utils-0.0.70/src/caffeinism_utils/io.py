import threading
from collections import deque


class PopIO:
    def __init__(self):
        self.deque = deque()
        self.closed = False

    def write(self, data):
        self.deque.append(data)

    def pop(self):
        while self.deque:
            yield self.deque.popleft()

    def pop_all(self):
        ret = []
        while self.deque:
            ret.append(self.deque.popleft())

        return b"".join(ret)

    def tell(self):
        pass

    def seekable(self):
        return False


class QueueIO:
    _exc: Exception

    def __init__(self):
        self._buffer = bytearray()
        self._data_available = threading.Condition(threading.Lock())
        self._eof = False
        self._exc = None
        self.closed = False

    def write(self, data: bytes):
        with self._data_available:
            self._buffer.extend(data)
            self._data_available.notify_all()

    def read(self, size: int = -1) -> bytes:
        with self._data_available:
            while True:
                if self._exc is not None:
                    raise self._exc

                if size == -1:
                    size = len(self._buffer)

                ret = bytes(memoryview(self._buffer)[:size])

                if ret:
                    del self._buffer[:size]
                    return ret

                if self._eof:
                    return b""

                self._data_available.wait()

    def close(self):
        with self._data_available:
            self._eof = True
            self._data_available.notify_all()

    def seekable(self):
        return False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def exc(self, exc):
        with self._data_available:
            self._exc = exc
            self._data_available.notify_all()
