# light.py

class Light:
    def __init__(self, name: str):
        self._name = name
        self._status = False

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def get_status(self) -> bool:
        return self._status

    def enable(self):
        if self._status == True:
            print('light already on')
        else:
            self._status = True

    def disable(self):
        if self._status == False:
            print('light already off')
        else:
            self._status = False