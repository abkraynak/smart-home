from message import Message

if __name__ == '__main__':
    mess = Message()
    print(mess)
    mess.setType('MENU')
    mess.addLine('1. option 1')
    mess.addLine('2. option 2')
    print(mess)
    mess2 = Message()
    print(mess2)
    mess2.unmarshal(mess.marshal())
    print(mess2)
    mess2.addParam('user', 'admin')

    mess3 = Message()
    mess3.unmarshal(mess2.marshal())
    print(mess3)
    print('Test Body')
    
    print(mess3.getBody())