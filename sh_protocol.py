# sh_protocol.py

import socket
from message import Message

class SHProtocol(object):
    CRLF = '\r\n'
    BUFSIZE = 8196

    def __init__(self, s: socket):
        self._sock = s
        self._rfile = self._sock.makefile(mode='r', encoding='utf-8', newline='\n')

    def _receive_line(self) -> str:
        line = self._rfile.readline()
        return line

    def put_message(self, mess: Message):
        message_string = mess.marshal()
        self._sock.sendall(message_string.encode('utf-8'))

    def get_message(self) -> Message:
        message_lines = []

        # Get first 2 lines that contain type and parameter (lines)
        message_lines.append(self._receive_line())
        message_lines.append(self._receive_line())
        
        m = Message()
        message_header = ''.join(message_lines)
        m.unmarshal(message_header)
        num_lines = int(m.get_parameter('lines'))
        
        # Get the remaining lines of the message (body)
        counter = 0
        while counter < num_lines:
            body_line = self._receive_line()
            m.add_line(body_line)
            counter += 1

        return m

    def close(self):
        self._sock.close()