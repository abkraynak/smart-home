# sh_protocol.py

import socket
from message import Message

class SHProtocol(object):
    CRLF = '\r\n'
    BUFSIZE = 8196

    def __init__(self, s: socket):
        self._sock = s
        self._rfile = self._sock.makefile(mode='r', encooding='utf-8', newline=SHProtocol.CRLF)

    def _receive_line(self) -> str:
        s = self._rfile.readline()
        return s

    def put_message(self, message: Message):
        data = message.marshal()
        self._sock.sendall(data.encode('utf-8'))

    def get_message(self) -> Message:
        lines = []

        # Get first 2 lines that contain type and parameter (lines)
        lines.append(self._receive_line())
        lines.append(self._receive_line())
        m = Message()
        m.unmarshal(''.join(lines))
        count = int(m.getParam('lines'))

        # Get the remaining lines of the message (body)
        for i in range(count):
            m.addLine(self._receive_line())

        return m

