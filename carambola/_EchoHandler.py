'''
Created on 29/05/2013

@author: pablo
'''

import asyncore
import logging
 
logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(msecs)d %(levelname)8s %(thread)d %(name)s %(message)s")

SIZE                    = 1024
 
class EchoHandler(asyncore.dispatcher):
 
    def __init__(self, conn_sock, client_address, server):
        self.log = logging.getLogger(__name__)
        self.server             = server
        self.client_address     = client_address
        self.buffer             = bytes("", "ascii")
 
        # We dont have anything to write, to start with
        self.is_writable        = False
 
        # Create ourselves, but with an already provided socket
        asyncore.dispatcher.__init__(self, conn_sock)
        self.log.debug("created handler; waiting for loop")
 
    def readable(self):
        return True     # We are always happy to read
 
    def writable(self):
        return self.is_writable # But we might not have
                                # anything to send all the time
 
    def handle_read(self):
        self.log.debug("handle_read")
        data = self.recv(SIZE)
        self.log.debug("after recv")
        if data:
            self.log.debug("got data")
            self.log.debug(data);
            self.buffer += data
            self.is_writable = True  # sth to send back now
        else:
            self.log.debug("got null data")
 
    def handle_write(self):
        self.log.debug("handle_write")
        if self.buffer:
            sent = self.send(self.buffer)
            self.log.debug("sent data")
            self.buffer = self.buffer[sent:]
        else:
            self.log.debug("nothing to send")
        if len(self.buffer) == 0:
            self.is_writable = False
 
    # Will this ever get called?  Does loop() call
    # handle_close() if we called close, to start with?
    def handle_close(self):
        self.log.debug("handle_close")
        self.log.info("conn_closed: client_address=%s:%s" % \
                     (self.client_address[0],
                      self.client_address[1]))
        self.close()
        #pass