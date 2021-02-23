from message import Message

if __name__ == '__main__':
    m0 = Message()
    print(m0)

    m1 = Message()
    print(m1)
    m1.setType('MENU')
    m1.addLine('Main Menu')
    m1.addLine('1. Alarm')
    m1.addLine('2. Lights')
    m1.addLine('3. Locks')
    m1.addLine('4. Logout')
    print(m1)

    m2 = Message()
    print(m2)
    m2.unmarshal(m1.marshal())
    print(m2)
    m2.addParam('user', 'admin')
    m2 = m2.marshal()

    m3 = Message()
    m3.unmarshal(m2)
    print(m3)
    
    print('Test Body')
    print(m3.getBody())