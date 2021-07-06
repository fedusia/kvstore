# coding: utf-8


class Storage:
    """
    Dependency Injection pattern
    """

    def __init__(self, engine):
        self.engine = engine

    def get(self, key):
        return self.engine.get(key)

    def set(self, key, value):
        return self.engine.set(key, value)
