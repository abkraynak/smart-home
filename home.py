from alarm import Alarm
from lock import Lock

class Home(object):
    def __init__(self, firstName: str, address: str):
        self._firstName = firstName
        self._address = address
        self._alarm = Alarm(0)
        self._locks = []

    def add_lock(self, name: str, pin: int):
        new_lock = Lock(name, pin)
        self._locks.append(new_lock)
    
    def print_locks(self):
        for lock in self._locks:
            print(lock._name, lock._enable, sep =' - ')
