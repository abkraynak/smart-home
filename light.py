# light.py

class Light:
    def __init__(self, name: str):
        self._name = name
        self._status = False
        self._color = {'R': 0, 'G': 0, 'B': 0}

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def get_color(self):
        return self._colors

    def set_color(self, red: int, green: int, blue: int):
        self._colors['R'] = red
        self._colors['G'] = green
        self._colors['B'] = blue

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