import threading


class Storage:
    def __init__(self, engine):
        self.engine = engine

    def get(self, key):
        return self.engine.get(key)

    def set(self, key, value):
        return self.engine.set(key, value)


class InMemStorage:
    def __init__(self):
        self.data = {}
        self.lock = threading.RLock()

    def set(self, key, value):
        with self.lock:
            self.data[key] = value
            return "{}={} is saved".format(key, value)

    def get(self, key):
        with self.lock:
            if key not in self.data.keys():
                return "{} not found".format(key)
            return self.data[key]
