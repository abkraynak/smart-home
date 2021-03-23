# lock.py

class Lock:
    def __init__(self, name: str, pin: int):
        self._name = name
        self._pin = pin
        self._enable = False

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def get_pin(self) -> int:
        return self._pin

    def set_pin(self, pin: int):
        self._pin = pin

    def get_status(self) -> bool:
        return self._enable

    def toggle(self, pin: int) -> bool:
        if pin == self.get_pin():
            self._enable = not self._enable
            return True
        else:
            return False
    
    def enable(self, pin: int):
        if self._enable == False:
            if pin == self.get_pin():
                self._enable = True
    
    def disable(self, pin: int):
        if self._enable == True:
            if pin == self.get_pin():
                self._enable = False