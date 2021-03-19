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

    def toggle(self, pin: int):
        if pin == self.get_pin():
            self._enable = not self._enable
        else:
            print('incorrect pin')
    
    def enable(self, pin: int):
        if self._enable == True:
            print('lock already on')
        else:
            if pin == self.get_pin():
                print('pins match')
                self._enable = True
            else:
                print('incorrect pin')
    
    def disable(self, pin: int):
        if self._enable == False:
            print('lock already disabled')
        else:
            if pin == self.get_pin():
                print('pins match')
                self._enable = False
            else:
                print('incorrect pin')