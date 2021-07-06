from kvstorage.core import Storage
from kvstorage.storage import InMemStorage


def hello_world():
    return "<p>Hello world</p>"


def getter(key):
    storage = Storage(InMemStorage())
    body = storage.get(key)
    return body


def set_wrap(storage):
    def setter(key, value):
        body = storage.set(key, value)
        return body

    return setter
