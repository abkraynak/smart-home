class Alarm:
    def __init__(self, pin: int):
        self._pin = pin
        self._enable = False

    def get_pin(self) -> int:
        return self._pin

    def set_pin(self, pin: int):
        self._pin = pin 