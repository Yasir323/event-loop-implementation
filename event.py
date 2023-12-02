class Event:

    def __init__(self, key: str, data: str, asynchronous: bool):
        self.key = key
        self.data = data
        self.asynchronous = asynchronous
