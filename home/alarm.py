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

    def enable(self, pin: int):
        if self._enable == True:
            print('alarm already on')
        else:
            if pin == self.get_pin():
                print('pins match')
                self._enable = True
            else:
                print('incorrect pin')

    def disable(self, pin: int):
        if self._enable == False:
            print('alarm already disabled')
        else:
            if pin == self.get_pin():
                print('pins match')
                self._enable = False
            else:
                print('incorrect pin')