# sh_protocol.py

import socket
from message import Message

class SHProtocol(object):
    CRLF = '\r\n'
    BUFSIZE = 8196

    def __init__(self, s: socket):
        self._sock = s
        self._rfile = self._sock.makefile(mode='r', encooding='utf-8',newline=SHProtocol.CRLF)

    