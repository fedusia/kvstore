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


class PrintLogic:
    def __init__(self, print_func=print):
        self.print_func = print_func

    def show(self):
        self.print_func.show()


class JustPrint:
    def __init__(self, data):
        self.data = data

    def show(self):
        print(self.data)
