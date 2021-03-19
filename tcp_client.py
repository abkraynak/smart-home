# tcp_client.py

import socket
from sh_protocol import SHProtocol
from sh_client import SHClient
    
HOST = "localhost"
PORT = 50001

if __name__ == "__main__":
    # Create the socket
    # Defaults family=AF_INET, type=SOCK_STREAM, proto=0, filno=None
    commsoc = socket.socket()
    
    # Connect to localhost:50001
    commsoc.connect((HOST, PORT))
    
    # Run the application protocol
    shp = SHProtocol(commsoc)
    shc = SHClient(shp)
    shc.run()
    
    # Close the comm socket
    commsoc.close()