# home.py

from alarm import Alarm
from light import Light
from lock import Lock

class Home(object):
    def __init__(self, firstName: str, address: str):
        self._firstName = firstName
        self._address = address
        self._alarm = Alarm(0)
        self._lights = []
        self._locks = []

    def add_light(self, name: str):
        new_light = Light(name)
        self._lights.append(new_light)

    def get_light_color(self, name: str):
        for light in self._lights:
            if light._name == name:
                light.get_color()

    def set_light_color(self, name: str, r: int, g: int, b: int):
        for light in self._lights:
            if light._name == name:
                light.set_color(r, g, b)

#    def get_light_status(self, name: str):

    
#    def enable_light(self, name: str):

    
 #   def disable_light(self, name: str):


    def print_lights(self):
        for light in self._lights:
            print(light._name, light._status, light._color, sep = ' - ')

    def add_lock(self, name: str, pin: int):
        new_lock = Lock(name, pin)
        self._locks.append(new_lock)

    def print_locks(self):
        for lock in self._locks:
            print(lock._name, lock._enable, sep = ' - ')

