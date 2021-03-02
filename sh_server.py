# sh_server.py

from message import Message
from sh_protocol import SHProtocol

class SHServer(object):
    def __init__(self, s: SHProtocol):
        self._shp = s
        
    def run(self):
        m0_recv = self._shp.get_message()
        print(m0_recv)

        # First message sent is username request
        m1_send = Message()
        m1_send.setType('USER')
        m1_send.addParam('user', 'none')
        m1_send.addLine('Enter username:')
        self._shp.put_message(m1_send)

        