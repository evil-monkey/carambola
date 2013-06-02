'''
Created on 29/05/2013

@author: pablo
'''

import asyncore
import logging
 
logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(msecs)d %(levelname)8s %(thread)d %(name)s %(message)s")

SIZE = 1024
 
class EchoHandler(asyncore.dispatcher):
 
    def __init__(self, conn_sock, client_address, server):
        self.log = logging.getLogger(__name__)
        self.server = server
        self.client_address = client_address
        self.incoming_buffer = bytes("", "ascii")
        self.outcoming_buffer = bytes("", "ascii")
        self.broadcast_buffer = bytes("", "ascii")
        
        # We dont have anything to write, to start with
        self.is_writable = False
 
        # Create ourselves, but with an already provided socket
        asyncore.dispatcher.__init__(self, conn_sock)
        self.log.debug("created handler; waiting for loop")
 
    def readable(self):
        return True  # We are always happy to read
 
    def writable(self):
        return self.is_writable  # But we might not have
                                # anything to send all the time
 
    def handle_read(self):
        self.log.debug("handle_read")
        data = self.recv(SIZE)
        self.log.debug("after recv")
        if data:
            self.log.debug("got data")
            self.log.debug(data);
            #TODO: develop command parser and strategies...
            self.incoming_buffer += data
            self.outcoming_buffer += data
            self.broadcast_buffer += data
            self.is_writable = True  # sth to send back now
        else:
            self.log.debug("got null data")
 

    def echo(self):
        if self.incoming_buffer:
            sent = self.send(self.incoming_buffer)
            self.log.debug("sent echo")
            self.incoming_buffer = self.incoming_buffer[sent:]
        else:
            self.log.debug("no echo to send")
        if len(self.incoming_buffer) == 0:
            self.is_writable = False
            
    def say(self, buffer):
        if buffer:
            self.send(buffer)
            self.log.debug("sent buffer")
        else:
            self.log.debug("nothing to say")
        self.is_writable = False
            
    def broadcast(self):
        if self.broadcast_buffer:
            self.server.broadcast(self.broadcast_buffer, self)
            sent = self.send(self.broadcast_buffer)
            self.log.debug("broadcasted data")
            self.broadcast_buffer = self.broadcast_buffer[sent:]
        else:
            self.log.debug("nothing to broadcast")
        if len(self.broadcast_buffer) == 0:
            self.is_writable = False
            
    def whisper(self):
        if self.outcoming_buffer:
            sent = self.send(self.outcoming_buffer)
            self.log.debug("whispered data")
            self.outcoming_buffer = self.outcoming_buffer[sent:]
        else:
            self.log.debug("nothing to whisper")
        if len(self.outcoming_buffer) == 0:
            self.is_writable = False

    def handle_write(self):
        self.log.debug("handle_write")
        self.broadcast()
        
 
    # Will this ever get called?  Does loop() call
    # handle_close() if we called close, to start with?
    def handle_close(self):
        self.log.debug("handle_close")
        self.log.debug("conn_closed: client_address=%s:%s" % \
                     (self.client_address[0],
                      self.client_address[1]))
        self.close()
        # pass
    
    def equals(self, obj):
        if (obj is not None and type(obj) == type(self)) :
            return self.client_address[0] == obj.client_address[0] and self.client_address[1] == obj.client_address[1]
        return False;
