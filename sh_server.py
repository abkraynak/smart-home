# sh_server.py

from message import Message
from sh_protocol import SHProtocol
from home import Home

message_break = '-----------------------------'

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
                m_send.add_line(message_break)
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
            menu = [message_break, '[0] Logout', '[1] Alarms', '[2] Lights', '[3] Locks']
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
            menu = [message_break, '[0] Main Menu', '[1] Get status', '[2] Enable', '[3] Disable', '[4] Change PIN']
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
            m_send.add_line('Color is R=' + str(self._home._lights[room]._color['R']) + ', G=' + str(self._home._lights[room]._color['G']) + ', B=' + str(self._home._lights[room]._color['B']))
        else:
            m_send.add_line(self._home._lights[room]._name + ' light is DISABLED')
        
        self._shp.put_message(m_send)
    
    def _get_lights_room(self) -> int:
        menu = [message_break, '[0] Main Menu', '[1] Show all status', '[2] Enable all', '[3] Disable all', ' ', 'Or select a room:']
        diff = num_lights = 4
        for light in self._home._lights:
            menu.append('[' + str(num_lights) + '] ' + light._name)
            num_lights += 1
        m_send = Message()
        m_send.set_type('MENU')
        m_send.add_parameter('label', 'room')
        m_send.add_lines(menu)
        self._shp.put_message(m_send)

        m_recv = self._shp.get_message()
        room = int(m_recv.get_parameter('room'))
        return room, num_lights, diff
    
    def _lights_menu(self):
        try:
            room, i, diff = self._get_lights_room()
            if room == 0:
                self._menu_path = '/main'
            elif room == 1:
                m_send = Message()
                m_send.set_type('DISPLAY')
                for L in self._home._lights:
                    if L._status:
                        m_send.add_line('- ' + L._name + ' light is ENABLED')
                        m_send.add_line('    Brightness level is ' + str(L._brightness) + '%')
                        m_send.add_line('    Color is R=' + str(L._color['R']) + ', G=' + str(L._color['G']) + ', B=' + str(L._color['B']))
                    else:
                        m_send.add_line('- ' + L._name + ' light is DISABLED')
                    
                self._shp.put_message(m_send)

            elif room == 2: 
                m_send = Message()
                m_send.set_type('DISPLAY')

                for L in self._home._lights:
                    L.enable()
                    
                m_send.add_line('All lights enabled!')
                self._shp.put_message(m_send)

            elif room == 3:
                m_send = Message()
                m_send.set_type('DISPLAY')

                for L in self._home._lights:
                    L.disable()
                    
                m_send.add_line('All lights disabled!')
                self._shp.put_message(m_send)

            elif room <= i:
                # Find what the next choice
                menu = [message_break, '[0] Back', '[1] Get status', '[2] Enable', '[3] Disable', '[4] Adjust brightness', '[5] Adjust color']
                
                m_send = Message()
                m_send.set_type('MENU')
                m_send.add_parameter('label', 'choice')
                m_send.add_lines(menu)
                self._shp.put_message(m_send)

                m_recv = self._shp.get_message()
                choice = m_recv.get_parameter('choice')

                if choice == '0':
                    self._menu_path = '/main/lights'
                
                elif choice == '1':
                    # Status
                    self._light_status(room - diff)
                    self._menu_path = '/main/lights'

                elif choice == '2' or choice == '3':
                    # Toggle
                    self._home._lights[room - diff].toggle()
                    self._light_status(room - diff)

                elif choice == '4':
                    # Adjust brightness
                    m_send = Message()
                    m_send.set_type('MENU')
                    m_send.add_parameter('label', 'brightness')
                    m_send.add_line('Enter desired brightness level (0 to 100) : ')
                    self._shp.put_message(m_send)

                    m_recv = self._shp.get_message()
                    brightness = int(m_recv.get_parameter('brightness'))
                    self._home._lights[room - diff].set_brightness(brightness)

                    m_send.clear()
                    m_send.set_type('DISPLAY')
                    m_send.add_line('Brightness successfully changed!')
                    self._shp.put_message(m_send)

                elif choice == '5':
                    # Adjust color
                    m_send = Message()
                    m_send.set_type('MENU')
                    m_send.add_parameter('label', 'rgb')
                    m_send.add_line('Enter desired RGB values (0 to 255) : ')
                    self._shp.put_message(m_send)

                    m_recv = self._shp.get_message()
                    rgb = m_recv.get_parameter('rgb')
                    r, g, b = rgb.split()
                    self._home._lights[room - diff].set_color(int(r), int(g), int(b))
                    
                    m_send.clear()
                    m_send.set_type('DISPLAY')
                    m_send.add_line('Color successfully changed!')
                    self._shp.put_message(m_send)

                else:
                    self._menu_path = '/main'

            else:
                self._menu_path = '/main'

        except Exception as e:
            print('_lights_menu():', e)
            self.shutdown()

        else:
            return

    def _get_lock_name(self):
        menu = [message_break, '[0] Main Menu', '[1] Show all status', ' ', 'Or select a lock:']
        diff = num_locks = 2
        for lock in self._home._locks:
            menu.append('[' + str(num_locks) + '] ' + lock._name)
            num_locks += 1
        
        m_send = Message()
        m_send.set_type('MENU')
        m_send.add_parameter('label', 'lock')
        m_send.add_lines(menu)
        self._shp.put_message(m_send)

        m_recv = self._shp.get_message()
        lock = int(m_recv.get_parameter('lock'))
        return lock, num_locks, diff
    
    def _get_lock_status(self, lock: int):
        m_send = Message()
        m_send.set_type('DISPLAY')

        if self._home._locks[lock]._enable:
            m_send.add_line(self._home._locks[lock]._name + ' lock is LOCKED')
        else:
            m_send.add_line(self._home._locks[lock]._name + ' lock is UNLOCKED')

        self._shp.put_message(m_send)
    
    def _locks_menu(self):
        try:
            lock, i, diff = self._get_lock_name()
            if lock == 0:
                self._menu_path = '/main'
            elif lock == 1:
                m_send = Message()
                m_send.set_type('DISPLAY')
                for L in self._home._locks:
                    if L._enable:
                        m_send.add_line('- ' + L._name + ' is LOCKED')
                    else:
                        m_send.add_line('- ' + L._name + ' is UNLOCKED')
                    
                self._shp.put_message(m_send)

            elif lock <= i:
                # Find what the next choice
                menu = ['[0] Back', '[1] Get status', '[2] Lock', '[3] Unlock', '[4] Manage PINs']
                
                m_send = Message()
                m_send.set_type('MENU')
                m_send.add_parameter('label', 'choice')
                m_send.add_lines(menu)
                self._shp.put_message(m_send)

                m_recv = self._shp.get_message()
                choice = m_recv.get_parameter('choice')

                if choice == '0':
                    self._menu_path = '/main/locks'
                elif choice == '1':
                    # Status
                    self._get_lock_status(lock - diff)
                    self._menu_path = '/main/locks'

                elif choice == '2' or choice == '3':
                    # Toggle
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
                            pin = int(m_recv.get_parameter('pin'))

                            count += 1
                            if count > 2:
                                    raise Exception('Too many PIN entry attempts')

                            if self._home._locks[lock - diff].toggle(pin):
                                match = True
                                self._get_lock_status(lock - diff)
                                self._menu_path = '/main/locks'

                    except Exception as e:
                        print('_locks_menu(): toggle: ', e)
                        self.shutdown()

                elif choice == '4':
                    # Manage PINs
                    self._get_lock_status(lock - diff)
                    self._menu_path = '/main/locks'

                else:
                    self._menu_path = '/main'

            else:
                self._menu_path = '/main'

        except Exception as e:
            print('_locks_menu():', e)
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
                      '/main/lights': self._lights_menu,
                      '/main/locks': self._locks_menu }

        while self._loggedin:
            f = menu_pages[self._menu_path]
            f()