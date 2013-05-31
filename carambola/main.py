'''
Created on 29/05/2013

@author: pablo
'''
import carambola

if __name__ == '__main__':
    pass

import asyncore
import logging

from carambola._EchoServer import EchoServer
from carambola._EchoClient import EchoClient

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

address = ('localhost', 0) # let the kernel give us a port

#server = EchoServer(address)

interface = "0.0.0.0"
port = 8080
server = EchoServer((interface, port))
server.serve_forever()

ip, port = server.address # find out what port we were given
logging.debug(port)
#message_data = open('lorem.txt', 'r').read()
#client = EchoClient(ip, port, message="holaholaholaholaholaholaholaholaholaholaholaholaholaholaholaholaholaholaholaholaholaholaholahola!")
asyncore.loop()