# sh_client.py

from message import Message
from sh_protocol import SHProtocol

class SHClient(object):
    def __init__(self, s: SHProtocol):
        self._shp = s

    def run(self):
        # Send start message to server
        m_send0 = Message()
        m_send0.set_type('START')
        print('client made start message')
        print(m_send0)
        self._shp.put_message(m_send0)
        print('client sent start message')

        # Receive username request from server
        print('waiting to receive message')
        m_recv0 = self._shp.get_message()
        print(m_recv0.get_body())
        print('message received from server')

        # Input and send username
        username = input('>> ')
        m_send1 = Message()
        m_send1.set_type('CHOICE')
        m_send1.add_parameter('user', username)
        self._shp.put_message(m_send1)

        # Receive password request from server
        m_recv1 = self._shp.get_message()
        print(m_recv1.get_body())
        print('message received from server')

        # Input and send password
        password = input('>>')
        m_send2 = Message()
        m_send2.set_type('CHOICE')
        m_send2.add_parameter('pass', password)
        self._shp.put_message(m_send2)