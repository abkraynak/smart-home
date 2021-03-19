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
    
    def _alarms_menu(self):
        try:
            menu = ['0 - Main Menu', '1 - Get status', '2 - Enable', '3 - Disable', '4 - Change PIN']
            options = {'1': '/status', '2': '/toggle', '3': '/toggle', '4': '/change_pin'}
            m_send = Message()
            m_send.set_type('MENU')
            m_send.add_parameter('label', 'choice')
            m_send.add_lines(menu)
            self._shp.put_message(m_send)

            m_recv = self._shp.get_message()
            choice = m_recv.get_parameter('choice')

            if choice == '0':
                self._menu_path = '/main'
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
        match = False
        try:
            while not match:
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
                    match = True
                    self._home._alarm.toggle(int(pin))
                    self._alarm_status()


        except Exception as e:
            print('_alarm_toggle():', e)
            self.shutdown()

        else:
            return

    def _alarm_change_pin(self):
        count = 0
        current_match = False
        try:
            while not current_match:
                # Enter current PIN
                m_send = Message()
                m_send.set_type('MENU')
                m_send.add_parameter('label', 'pin0')
                m_send.add_line('Enter current PIN : ')
                self._shp.put_message(m_send)

                m_recv = self._shp.get_message()
                pin0 = m_recv.get_parameter('pin0')

                count += 1
                if count > 2:
                        raise Exception('Too many PIN entry attempts')

                # Verify current PIN is correct
                if int(pin0) == self._home._alarm.get_pin():
                    current_match = True
        
        except Exception as e:
            print('_alarm_change_pin():', e)
            self.shutdown()

        else:
            # Ask for new PIN
            m_send.clear()
            m_send.set_type('MENU')
            m_send.add_parameter('label', 'pin1')
            m_send.add_line('Enter new PIN : ')
            self._shp.put_message(m_send)

            m_recv = self._shp.get_message()
            pin1 = m_recv.get_parameter('pin1')

            # Ask for new PIN (again)
            m_send.clear()
            m_send.set_type('MENU')
            m_send.add_parameter('label', 'pin2')
            m_send.add_line('Enter new PIN (again) : ')
            self._shp.put_message(m_send)

            m_recv = self._shp.get_message()
            pin2 = m_recv.get_parameter('pin2')

            # Verify match
            if pin1 == pin2:
                self._home._alarm.set_pin(int(pin1))
                m_send.clear()
                m_send.set_type('DISPLAY')
                m_send.add_line('PIN successfully changed!')
                self._shp.put_message(m_send)
                self._menu_path = '/main/alarms'
    
    def _light_status(self, room: int):
        m_send = Message()
        m_send.set_type('DISPLAY')

        if self._home._lights[room]._status:
            m_send.add_line(self._home._lights[room]._name + ' light is ENABLED')
            m_send.add_line('Brightness level is ' + str(self._home._lights[room]._brightness) + '%')
            m_send.add_line('Color is R=' + str(self._home._lights[room]._color['R']) + ', G= ' + str(self._home._lights[room]._color['G']) + ', B= ' + str(self._home._lights[room]._color['B']))
        else:
            m_send.add_line(self._home._lights[room]._name + ' light is DISABLED')
        

        self._shp.put_message(m_send)
    
    def _get_lights_room(self) -> int:
        menu = ['0 - Main Menu']
        num_lights = 1
        for light in self._home._lights:
            menu.append(str(num_lights) + ' - ' + light._name)
            num_lights += 1
        m_send = Message()
        m_send.set_type('MENU')
        m_send.add_parameter('label', 'room')
        m_send.add_lines(menu)
        self._shp.put_message(m_send)

        m_recv = self._shp.get_message()
        room = int(m_recv.get_parameter('room'))
        return room, num_lights
    
    def _lights_menu(self):
        try:
            room, i = self._get_lights_room()
            if room == 0:
                self._menu_path = '/main'
            elif room <= i:
                # Find what the next choice
                menu = ['0 - Main Menu', '1 - Get status', '2 - Enable', '3 - Disable', '4 - Adjust brightness', '5 - Adjust color']
                
                m_send = Message()
                m_send.set_type('MENU')
                m_send.add_parameter('label', 'choice')
                m_send.add_lines(menu)
                self._shp.put_message(m_send)

                m_recv = self._shp.get_message()
                choice = m_recv.get_parameter('choice')

                if choice == '0':
                    self._menu_path = '/main'
                
                elif choice == '1':
                    # Status
                    self._light_status(room - 1)
                    self._menu_path = '/main/lights'

                elif choice == '2' or choice == '3':
                    # Toggle
                    self._home._lights[room - 1].toggle()
                    self._light_status(room - 1)

                elif choice == '4':
                    # Adjust brightness
                    m_send = Message()
                    m_send.set_type('MENU')
                    m_send.add_parameter('label', 'brightness')
                    m_send.add_line('Enter desired brightness level (0 to 100) : ')
                    self._shp.put_message(m_send)

                    m_recv = self._shp.get_message()
                    brightness = int(m_recv.get_parameter('brightness'))
                    self._home._lights[room - 1].set_brightness(brightness)

                elif choice == '5':
                    # Adjust color
                    print(self._home._lights[room - 1]._name)

                else:
                    self._menu_path = '/main'

            else:
                self._menu_path = '/main'

        except Exception as e:
            print('_lights_menu():', e)
            self.shutdown()

        else:
            return

    def welcome_message(self):
        m_send = Message()
        m_send.set_type('DISPLAY')
        m_send.add_line('Welcome, ' + self._home._first_name)
        self._shp.put_message(m_send)
    
    def run(self):
        # Receive the start message from client
        m_recv = self._shp.get_message()

        self._login()
        if self._loggedin:
            self.welcome_message()

        menu_pages = {'/main': self._main_menu,
                      '/main/logout': self.shutdown,
                      '/main/alarms': self._alarms_menu,
                      '/main/alarms/status': self._alarm_status,
                      '/main/alarms/toggle': self._alarm_toggle,
                      '/main/alarms/change_pin': self._alarm_change_pin,
                      '/main/lights': self._lights_menu
                      }

        while self._loggedin:
            print(self._menu_path)
            f = menu_pages[self._menu_path]
            f()