# message_test.py

from message import Message

if __name__ == '__main__':
    m0 = Message()
    print(m0)

    m1 = Message()
    print(m1)
    print(m1.get_type())
    m1.set_type('MENU')
    print(m1.get_type())
    m1.add_parameter('1', 'username')
    m1.add_line('Main Menu')
    m1.add_line('1. Alarm')
    m1.add_line('2. Lights')
    m1.add_line('3. Locks')
    m1.add_line('4. Logout')
    print(m1)
    print(m1.get_body())

    m2 = Message()
    print(m2)
    m2.unmarshal(m1.marshal())
    print(m2)
    m2.add_parameter('user', 'admin')
    m2 = m2.marshal()

    m3 = Message()
    m3.unmarshal(m2)
    print(m3)
    
    print('Test Body')
    print(m3.get_body())