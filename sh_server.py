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
            menu = ['0 - Logout', '1 - Get status', '2 - Enable', '3 - Disable', '4 - Change PIN']
            options = {'1': '/status', '2': '/toggle', '3': '/toggle', '4': '/change_pin'}
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
    
    def _alarm_status(self):
        m_send = Message()
        m_send.set_type('DISPLAY')

        if self._home._alarm.get_status():
            m_send.add_line('Alarm is ENABLED')
        else:
            m_send.add_line('Alarm is DISABLED')

        self._shp.put_message(m_send)
        self._menu_path = '/main/alarms'

    def _alarm_toggle(self):
        count = 0
        alarm_pin = False
        try:
            while not alarm_pin:
                m_send = Message()
                m_send.set_type('MENU')
                m_send.add_parameter('label', 'pin')
                m_send.add_line('Enter your PIN : ')

                self._shp.put_message(m_send)

                m_recv = self._shp.get_message()
                pin = m_recv.get_parameter('pin')
                
                count += 1
                if count > 2:
                        raise Exception('Too many PIN entry attempts')

                if int(pin) == self._home._alarm.get_pin():
                    alarm_pin = True
                    self._alarm_status()


        except Exception as e:
            print('_alarm_toggle():', e)
            self.shutdown()

        else:
            return

    def run(self):
        # Receive the start message from client
        m_recv = self._shp.get_message()

        self._login()
        if self._loggedin:
            print('Welcome, ', self._home._first_name)

        menu_pages = {'/main': self._main_menu,
                      '/main/logout': self.shutdown,
                      '/main/alarms': self._alarms_menu,
                      '/main/alarms/status': self._alarm_status,
                      '/main/alarms/toggle': self._alarm_toggle
                      }

        while self._loggedin:
            print(self._menu_path)
            f = menu_pages[self._menu_path]
            f()


        