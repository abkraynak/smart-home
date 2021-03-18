# sh_client.py

from message import Message
from sh_protocol import SHProtocol

class SHClient(object):
    def __init__(self, s: SHProtocol):
        self._shp = s

    def run(self):
        # Send start message to server
        m_send = Message()
        m_send.set_type('START')
        self._shp.put_message(m_send)

        try:
            while True:
                # Receive username request from server
                m_recv = self._shp.get_message()
                print(m_recv.get_body())

                # Input and send username
                username = input('>> ')
                m_send.clear()
                m_send.set_type('CHOICE')
                m_send.add_parameter('user', username)
                self._shp.put_message(m_send)

                # Receive password request from server
                m_recv = self._shp.get_message()
                print(m_recv.get_body())

                # Input and send password
                password = input('>>')
                m_send2 = Message()
                m_send2.set_type('CHOICE')
                m_send2.add_parameter('pass', password)
                self._shp.put_message(m_send2)
        except Exception:
            self._shp.close()