# sh_server.py

from message import Message
from sh_protocol import SHProtocol

class SHServer(object):
    def __init__(self, s: SHProtocol):
        self._shp = s
        
    def run(self):
        # Receive the first message from client
        print('waiting for message')
        m_recv = self._shp.get_message()
        print('message received! it is: ')
        print(m_recv)

        # First message sent is username request
        m_send = Message()
        m_send.set_type('USER')
        m_send.add_parameter('user', 'none')
        m_send.add_line('Enter username:')
        self._shp.put_message(m_send)

        # Receive username from client
        m_recv = self._shp.get_message()
        print(m_recv.get_parameter('user'))
        print('received username from client')

        # Send password request
        m_send = Message()
        m_send.set_type('PASS')
        m_send.add_parameter('pass', 'none')
        m_send.add_line('Enter password: ')
        self._shp.put_message(m_send)

        # Receive password from client
        m_recv = self._shp.get_message()
        print(m_recv.get_parameter('pass'))
        print('received password from client')


