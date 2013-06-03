import asyncore
import asynchat
import socket

# a simple chat room
class Room:
    
    def __init__(self):
        self.speakers = []

    def join(self, speaker):
        self.speakers.append( speaker )
        speaker.sendMsg('Welcome to Carambola')
    
    def leave(self, speaker):
        self.speakers.remove( speaker )
        speaker.sendMsg('bye')

    def speak(self, words):
        for s in self.speakers:
            s.sendMsg( words )

#connection handler
class Handler(asynchat.async_chat):
    def __init__(self, conn, room):
        asynchat.async_chat.__init__(self, sock=conn)
        self.in_buffer = []
        self.set_terminator(b"\r\n")
        
        self.room = room
        room.join(self)
  
    def collect_incoming_data(self, data):
        self.in_buffer.append(data)
 
    def found_terminator(self):
        line = (b''.join( self.in_buffer )).decode()
        if line == "QUIT":
            self.room.leave(self)
            self.close_when_done()
        else:
            self.room.speak( line )
            self.in_buffer = []

    def sendMsg(self, msg):
        self.push( msg.encode('utf-8') + self.terminator )

    def handle_error(self): 
         raise 

#async server handler
class Server(asynchat.async_chat):
    def __init__(self, room):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("127.0.0.1", 8080))
        self.listen(5)
        
        self.room = room
    
    def handle_accept(self):
        sock, addr = self.accept()
        client = Handler(sock, self.room)
 
    def handle_error(self): 
         raise 

#run
if __name__ == '__main__':
    room = Room()
    server = Server(room)
    asyncore.loop()
