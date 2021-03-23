# tcp_server.py

import socket
from sh_protocol import SHProtocol
from sh_server import SHServer
    
HOST = "localhost"
PORT = 50004

if __name__ == "__main__":
    # Create the server socket
    # Defaults family=AF_INET, type=SOCK_STREAM, proto=0, filno=None
    serversoc = socket.socket()
    
    # Bind to local host:5000`
    serversoc.bind((HOST, PORT))
                   
    # Make passive with backlog=5
    serversoc.listen(5)
    
    # Wait for incoming connections
    while True:
        print("Listening on ", PORT)
        
        # Accept the connection
        commsoc, raddr = serversoc.accept()
        
        # Run the application protocol
        shp = SHProtocol(commsoc)
        shs = SHServer(shp)
        shs.run()
        
        # Close the comm socket
        commsoc.close()
    
    # Close the server socket
    serversoc.close()