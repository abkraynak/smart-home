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
                # Receive from server
                m_recv = self._shp.get_message()
                print(m_recv.get_body())

                if m_recv.get_type() == 'DISPLAY':
                    continue

                # Send message to server
                user_input = input('>> ')
                m_send.clear()
                m_send.set_type('CHOICE')
                m_send.add_parameter(m_recv.get_parameter('label'), user_input)
                self._shp.put_message(m_send)

        except Exception:
            self._shp.close()