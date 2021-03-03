# sh_server.py

from message import Message
from sh_protocol import SHProtocol

class SHServer(object):
    def __init__(self, s: SHProtocol):
        self._shp = s
        
    def run(self):
        # Receive the first message from client
        m_recv0 = self._shp.get_message()
        print('message received! it is: ')
        print(m_recv0)
        print('done w first message')

        # First message sent is username request
        m_send0 = Message()
        m_send0.set_type('USER')
        m_send0.add_parameter('user', 'none')
        m_send0.add_line('Enter username:')
        self._shp.put_message(m_send0)

        # Receive username from client
        m_recv1 = self._shp.get_message()
        print(m_recv1.get_parameter('user'))
        print('received username from client')

        # Send password request
        m_send1 = Message()
        m_send1.set_type('PASS')
        m_send1.add_parameter('pass', 'none')
        m_send1.add_line('Enter password: ')
        self._shp.put_message(m_send1)

        # Receive password from client
        m_recv2 = self._shp.get_message()
        print(m_recv2.get_parameter('pass'))
        print('received password from client')