# alarm.py

class Alarm:
    def __init__(self, pin: int):
        self._pin = pin
        self._enable = False

    def get_pin(self) -> int:
        return self._pin

    def set_pin(self, pin: int):
        self._pin = pin

    def get_status(self) -> int:
        return self._enable

    def toggle(self, pin: int):
        if pin == self.get_pin():
           self._enable = not self._enable
                
    def enable(self, pin: int):
        if self._enable == False:
            if pin == self.get_pin():
                self._enable = True

    def disable(self, pin: int):
        if self._enable == True:
            if pin == self.get_pin():
                self._enable = False