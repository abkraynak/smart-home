# sh_server.py

from message import Message
from sh_protocol import SHProtocol
from home import Home

class SHServer(object):
    def __init__(self, s: SHProtocol):
        self._shp = s
        self._loggedin = False
        self._menu_path = '/main'
        self._home = Home('Andrew', 'SW 12th St')
        self._home.sample_home()
        
    def shutdown(self):
        self._loggedin = False 
        self._shp.close()
        return

    def _login(self):
        count = 0
        try:
            while not self._loggedin:
                m_send = Message()

                # First message sent is username request
                m_send.clear()
                m_send.set_type('USER')
                m_send.add_parameter('label', 'user')
                m_send.add_line('Enter username:')
                self._shp.put_message(m_send)

                # Receive username from client
                m_recv = self._shp.get_message()
                username = m_recv.get_parameter('user')

                # Send password request
                m_send.clear()
                m_send.set_type('PASS')
                m_send.add_parameter('label', 'pass')
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
            self.shutdown()

        else:
            return
    
    def _main_menu(self):
        try:
            menu = ['0 - Logout', '1 - Alarms', '2 - Lights', '3 - Locks']
            options = {'1': '/alarms', '2': '/lights', '3': '/locks'}
            m_send = Message()
            m_send.set_type('MENU')
            m_send.add_parameter('label', 'choice')
            m_send.add_lines(menu)
            self._shp.put_message(m_send)

            m_recv = self._shp.get_message()
            choice = m_recv.get_parameter('choice')

            if choice == 0:
                self._menu_path = '/main/logout'
            elif choice in options:
                self._menu_path += options[choice]
            else:
                self._menu_path = '/main'

        except Exception:
            self.shutdown()

        else:
            return
    
    def _alarms_menu(self):
        try:
            menu = ['0 - Logout', '1 - Get status', '2 - Enable', '3 - Disable']
            options = {'1': '/status', '2': '/enable', '3': '/disable'}
            m_send = Message()
            m_send.set_type('MENU')
            m_send.add_parameter('label', 'choice')
            m_send.add_lines(menu)
            self._shp.put_message(m_send)

            m_recv = self._shp.get_message()
            choice = m_recv.get_parameter('choice')

            if choice == '0':
                self._menu_path = '/main/logout'
            elif choice in options:
                self._menu_path += options[choice]
            else:
                self._menu_path = '/main'

        except Exception:
            self.shutdown()

        else:
            return
    
    def _alarms_status(self):
        if self._home._alarm.get_status():
            
    
    def run(self):
        # Receive the start message from client
        m_recv = self._shp.get_message()

        self._login()
        if self._loggedin:
            print('Welcome, ', self._home._first_name)

        menu_pages = {'/main': self._main_menu,
                      '/main/logout': self.shutdown,
                      '/main/alarms': self._alarms_menu,
                      '/main/alarms/status': self._alarms_status
                      '/main/alarrms/enable': 
                      '/main/alarms/disable': }

        while self._loggedin:
            print(self._menu_path)
            f = menu_pages[self._menu_path]
            f()


        