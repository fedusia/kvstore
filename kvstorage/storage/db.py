import threading


class InMemStorage:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()
        self.rlock = threading.RLock()

    def set(self, key, value):
        with self.lock:
            self.data[key] = value
            return "{}={} is saved".format(key, value)

    def get(self, key):
        with self.rlock:
            if key not in self.data.keys():
                return "{} not found".format(key)
            return self.data[key]
