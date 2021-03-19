# sh_server.py

from message import Message
from sh_protocol import SHProtocol
from home import Home

class SHServer(object):
    def __init__(self, s: SHProtocol):
        self._shp = s
        self._loggedin = False
        self._menu_level = 'main'
        self._home = Home('Andrew', 'SW 12th St')
        self._home.sample_home()
        
    def _login(self):
        count = 0
        try:
            while not self._loggedin:
                m_send = Message()

                # First message sent is username request
                m_send.clear()
                m_send.set_type('USER')
                m_send.add_parameter('1', 'user')
                m_send.add_line('Enter username:')
                self._shp.put_message(m_send)

                # Receive username from client
                m_recv = self._shp.get_message()
                username = m_recv.get_parameter('user')

                # Send password request
                m_send.clear()
                m_send.set_type('PASS')
                m_send.add_parameter('1', 'pass')
                m_send.add_line('Enter password: ')
                self._shp.put_message(m_send)

                # Receive password from client
                m_recv = self._shp.get_message()
                password = m_recv.get_parameter('pass')

                self._loggedin = self._home.authenticate(username, password)
                count += 1
                if count > 2:
                    raise Exception('Too many login attempts')

        except Exception as e:
            print('login():', e)

        else:
            return
    
    def run(self):
        # Receive the start message from client
        m_recv = self._shp.get_message()

        self._login()
        print('Welcome, ', self._home._first_name)