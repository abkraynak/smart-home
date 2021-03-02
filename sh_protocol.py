# sh_protocol.py

import socket
from message import Message

class SHProtocol(object):
    CRLF = '\n'
    BUFSIZE = 8196

    def __init__(self, s: socket):
        self._sock = s
        self._rfile = self._sock.makefile(mode='r', encoding='utf-8', newline=SHProtocol.CRLF)

    def _receive_line(self) -> str:
        s = self._rfile.readline()
        return s

    def put_message(self, mess: Message):
        data = mess.marshal()
        self._sock.sendall(data.encode('utf-8'))

    def get_message(self) -> Message:
        m_lines = []

        # Get first 2 lines that contain type and parameter (lines)
        m_lines.append(self._receive_line())
        m_lines.append(self._receive_line())
        
        m = Message()
        m.unmarshal(''.join(m_lines))
        count = int(m.get_parameter('lines'))

        # Get the remaining lines of the message (body)
        for i in range(count):
            m.add_line(self._receive_line())

        return m

    def close(self):
        self._sock.close()