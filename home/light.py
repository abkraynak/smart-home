# light.py

class Light:
    def __init__(self, name: str):
        self._name = name
        self._status = False
        self._color = {'R': 0, 'G': 0, 'B': 0}
        self._brightness = 0

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def get_color(self):
        return self._color

    def set_color(self, red: int, green: int, blue: int):
        self._color['R'] = red
        self._color['G'] = green
        self._color['B'] = blue

    def get_brightness(self):
        return self._brightness

    def set_brightness(self, level: int):
        if level in range(100):
            self._brightness = level
        else:
            print('incorrect value of brightness level')

    def get_status(self) -> bool:
        return self._status

    def toggle(self):
        self._status = not self._status
        if self._status:
            self._brightness = 100
        else:
            self._brightness = 0
    
    def enable(self):
        if self._status == True:
            print('light already on')
        else:
            self._status = True
            self._brightness = 100

    def disable(self):
        if self._status == False:
            print('light already off')
        else:
            self._status = False
            self._brightness = 0