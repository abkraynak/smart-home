from alarm import Alarm
from lock import Lock

class Home(object):
    def __init__(self, firstName: str, address: str):
        self._firstName = firstName
        self._address = address
        self._alarm = Alarm(0)
        self._locks = []

    
