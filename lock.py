class Lock:
    def __init__(self, name: str):
        self._name = name
        self._enable = False