class BaseKey(object):
    def __init__(self, type, key):
        self.type = type
        self.key = key

    @property
    def typed(self):
        return self.key + self.type

    def bytesWithoutType(self):
        return self.key.encode()

    def bytes(self):
        return self.typed.encode()
