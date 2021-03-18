# message.py

from enum import Enum

class Message(object):
    '''
    classdocs
    '''
    # Constants
    MCMDS = Enum('MCMDS', {'START': 'START', 'USER': 'USER','PASS': 'PASS',
                           'MENU': 'MENU', 'CHOICE': 'CHOICE', 'ERROR': 'ERROR'})
    CRLF = '\r\n'
    SPACE = ' '
    PJOIN = '&'
    VJOIN = '{}={}'
    VJOIN1 = '='
    
    def __init__(self):
        '''
        Constructor
        '''
        self._type = Message.MCMDS.START
        self._parameters = {'lines': '0'}
        self._body = []
        self._body_lines = 0
        
    def __str__(self) -> str:
        '''
        Stringify - marshal
        '''
        return self.marshal()
    
    def clear(self):
        self._type = Message.MCMDS.START
        self._parameters.clear()
        self._parameters = {'lines':'0'}
        self._body.clear()
        self._body_lines = 0

    def set_type(self, mtype: str):
        self._type = Message.MCMDS[mtype]
        
    def get_type(self) -> str:
        return self._type.value()

    def add_parameter(self, name: str, value: str):
        self._parameters[name] = value
        
    def get_parameter(self, name: str) -> str:
        return self._parameters[name]
    
    def add_line(self, line: str):
        self._body.append(line)
        self._body_lines += 1
        
    def add_lines(self, lines: list):
        for line in lines:
            self.add_line(line)
            
    def get_body(self) -> str:
        return Message.CRLF.join(self._body)
    
    def marshal(self) -> str:
        self._parameters['lines'] = str(self._body_lines)
        
        value = [self._type.value]
        pairs = [Message.VJOIN.format(k,v) for (k, v) in self._parameters.items()]
        parameters = Message.PJOIN.join(pairs)
        value.append(parameters)
        if len(self._body) > 0:
            value += self._body
        return '{}{}'.format(Message.CRLF.join(value), Message.CRLF)
    
    def unmarshal(self, value: str):
        self.clear()
        lines = value.split(Message.CRLF)
        self._type = Message.MCMDS[lines[0]]
        parameters = lines[1].split(Message.PJOIN)
        for p in parameters:
            k,v = p.split(Message.VJOIN1)
            self._parameters[k] = v
        self._body += lines[2:]
        self._body_lines = int(self._parameters['lines'])