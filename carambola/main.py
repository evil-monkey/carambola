'''
Created on 29/05/2013

@author: pablo
'''
if __name__ == '__main__':
    pass

import asyncore
import logging

from carambola.server._Server import Server

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

address = ('localhost', 0)  # let the kernel give us a port

# server = Server(address)

interface = "0.0.0.0"
port = 8080
server = Server((interface, port))
server.serve_forever()

ip, port = server.address  # find out what port we were given
logging.debug(port)

asyncore.loop()
