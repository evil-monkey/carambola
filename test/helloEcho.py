import asyncore
import asynchat
import socket

class Handler(asynchat.async_chat):
    def __init__(self, conn):
        asynchat.async_chat.__init__(self, sock=conn)
        self.in_buffer = []
        self.set_terminator(b"\r\n")
  
    def collect_incoming_data(self, data):
        self.in_buffer.append(data)
 
    def found_terminator(self):
        line = b''.join( self.in_buffer )
        if line == b"QUIT":
            self.close_when_done()
        else:
            self.push( line + self.terminator )
            self.in_buffer = []
    
    def handle_error(self): 
         raise 

class Server(asynchat.async_chat):
    def __init__(self):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("127.0.0.1", 8080))
        self.listen(5)
    
    def handle_accept(self):
        sock, addr = self.accept()
        client = Handler(sock)
 
    def handle_error(self): 
         raise 

if __name__ == '__main__':
    server = Server()
    asyncore.loop()
