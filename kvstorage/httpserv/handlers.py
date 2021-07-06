def hello_world():
    return "<p>Hello world</p>"


def getter(storage):
    def wrapped_getter(key):
        body = storage.get(key)
        return body

    return wrapped_getter


def setter(storage):
    def wrapped_setter(key, value):
        body = storage.set(key, value)
        return body

    return wrapped_setter
