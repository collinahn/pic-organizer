from threading import Lock


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class MetaSingletonThreaded(MetaSingleton):
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            return super().__call__(*args, **kwargs)
