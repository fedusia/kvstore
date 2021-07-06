from fastapi_jsonrpc import Entrypoint
from kvstorage.core.logic import Storage
from kvstorage.storage.db import InMemStorage


def hello_world() -> str:
    return "Hello World"


def getter(storage: Storage) -> str:
    def wrapped_getter(key) -> str:
        body = storage.get(key)
        return body

    return wrapped_getter


def setter(storage: Storage) -> str:
    def wrapped_setter(key, value) -> str:
        body = storage.set(key, value)
        return body

    return wrapped_setter


storage = Storage(engine=InMemStorage())

api_v1 = Entrypoint("/api/v1/jsonrpc")
api_v1.add_method_route(hello_world, name="say_hello")
api_v1.add_method_route(getter(storage), name="get")
api_v1.add_method_route(setter(storage), name="set")
