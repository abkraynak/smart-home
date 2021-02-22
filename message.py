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
        self._params = {'lines': '0'}
        self._body = []
        self._bodyLines = 0
        
    def __str__(self) -> str:
        '''
        Stringify - marshal
        '''
        return self.marshal()
    
    def setType(self, mtype: str):
        self._type = Message.MCMDS[mtype]
        
    def getType(self) -> str:
        return self._type.value()
    