'''
Created on 29/05/2013

@author: pablo
'''

import asyncore
import logging
import socket

from carambola._EchoHandler import EchoHandler

logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(msecs)d %(levelname)8s %(thread)d %(name)s %(message)s")

class EchoServer(asyncore.dispatcher):
    allow_reuse_address         = False
    request_queue_size          = 5
    address_family              = socket.AF_INET
    socket_type                 = socket.SOCK_STREAM
 
    def __init__(self, address, handlerClass=EchoHandler):
        self.log = logging.getLogger(__name__)
        self.address            = address
        self.handlerClass       = handlerClass
 
        asyncore.dispatcher.__init__(self)
        self.create_socket(self.address_family,
                               self.socket_type)
 
        if self.allow_reuse_address:
            self.set_reuse_addr()
 
        self.server_bind()
        self.server_activate()
 
    def server_bind(self):
        self.bind(self.address)
        self.log.debug("bind: address=%s:%s" % (self.address[0], self.address[1]))
 
    def server_activate(self):
        self.listen(self.request_queue_size)
        self.log.debug("listen: backlog=%d" % self.request_queue_size)
 
    def fileno(self):
        return self.socket.fileno()
 
    def serve_forever(self):
        asyncore.loop()
 
    # TODO: try to implement handle_request()
 
    # Internal use
    def handle_accepted(self, conn_sock, client_address):
        if self.verify_request(conn_sock, client_address):
            self.process_request(conn_sock, client_address)
 
    def verify_request(self, conn_sock, client_address):
        return True
 
    def process_request(self, conn_sock, client_address):
        self.log.info("conn_made: client_address=%s:%s" % \
                     (client_address[0],
                      client_address[1]))
        self.handlerClass(conn_sock, client_address, self)
 
    def handle_close(self):
        self.close()