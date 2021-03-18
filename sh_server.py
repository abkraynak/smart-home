# sh_server.py

from message import Message
from sh_protocol import SHProtocol
from home import Home

class SHServer(object):
    def __init__(self, s: SHProtocol):
        self._shp = s
        self._login = False
        self._home = Home('Andrew', 'SW 12th St')
        self._home.sample_home()
        
    def _login(self):
        # First message sent is username request
        m_send = Message()
        m_send.set_type('USER')
        m_send.add_parameter('user', 'none')
        m_send.add_line('Enter username:')
        self._shp.put_message(m_send)

        # Receive username from client
        m_recv = self._shp.get_message()
        username = m_recv.get_parameter('user')

        # Send password request
        m_send.clear()
        m_send.set_type('PASS')
        m_send.add_parameter('pass', 'none')
        m_send.add_line('Enter password: ')
        self._shp.put_message(m_send)

        # Receive password from client
        m_recv = self._shp.get_message()
        password = m_recv.get_parameter('pass')

        print(username)
        print(password)
    
    def run(self):
        # Receive the start message from client
        m_recv = self._shp.get_message()
        m_send = Message()
        
        while not self._login:
            # First message sent is username request
            m_send.clear()
            m_send.set_type('USER')
            m_send.add_parameter('user', 'none')
            m_send.add_line('Enter username:')
            self._shp.put_message(m_send)

            # Receive username from client
            m_recv = self._shp.get_message()
            username = m_recv.get_parameter('user')

            # Send password request
            m_send.clear()
            m_send.set_type('PASS')
            m_send.add_parameter('pass', 'none')
            m_send.add_line('Enter password: ')
            self._shp.put_message(m_send)

            # Receive password from client
            m_recv = self._shp.get_message()
            password = m_recv.get_parameter('pass')


            self._login = self._home.authenticate(username, password)
            print(self._login)

        print('outside loop')







