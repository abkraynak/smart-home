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
        m1_send.set_type('USER')
        m1_send.add_parameter('user', 'none')
        m1_send.add_line('Enter username:')
        self._shp.put_message(m1_send)

