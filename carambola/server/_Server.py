'''
Created on 29/05/2013

@author: pablo
'''

import asyncore
import logging
import socket

from carambola.server._ConnectionHandler import ConnectionHandler
from carambola.server._Room import Room

logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(msecs)d %(levelname)8s %(thread)d %(name)s %(message)s")

class Server(asyncore.dispatcher):
    
    MAIN_ROOM_ID = "general_chat"
    
    allow_reuse_address = False
    request_queue_size = 5
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    
 
    def __init__(self, address, handlerClass=ConnectionHandler):
        self.log = logging.getLogger(__name__)
        self.address = address
        self.handlerClass = handlerClass
        # default room 
        self.main_room = Room(self)
        self.main_room.is_private = False
        self.main_room.room_id = self.MAIN_ROOM_ID 
        # rooms info container
        self.rooms = {self.MAIN_ROOM_ID: self.main_room}
 
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
        self.log.debug("conn_made: client_address=%s:%s" % \
                     (client_address[0],
                      client_address[1]))
        self.main_room.add_member(
                    self.handlerClass(conn_sock, client_address, self))
 
    def handle_close(self):
        self.close()
    
    # Messages
    
    def broadcast(self, message, sender):
        ''' broadcast message to all server's connected clients
            Parameters
            ----------
            message : Buffer
                buffer containing the message to broadcast
               
            sender : ConnectionHandler
                sender's connection handler, this is ignored in broadcast
               
            Return
            ------
                void
        '''
        self.log.debug(message)
        for room_id in self.rooms.keys():
            self.room_broadcast(room_id, message, sender)
            
                
    def room_broadcast(self, room_id, message, sender = None):
        ''' broadcast message to all room connected clients
            Parameters
            ----------
            room_id : String
                room identifier
                
            message : Buffer
                buffer containing the message to broadcast
               
            sender : ConnectionHandler
                sender's connection handler, this is ignored in broadcast
               
            Return
            ------
                void
        '''
        self.log.debug(message)
        for session in self.rooms.get(room_id).members:
            if not session.equals(sender):
                session.say(message);
            
            
    # Commands handling
    
    def room_exists(self, room_id):
        ''' asks if server has a room with the provided id
            Parameters
            ----------
            room_id : String
               represent the room id
               
            Return
            ------
                boolean
        '''
        return self.rooms.__contains__(room_id)


    def add_room(self, room_id, session):
        ''' adds a new room to server's room pool
            Parameters
            ----------
            room_id : String
                represent the room id
               
            session : ConnectionHandler
                new room's creator
                
            Return
            ------
                void
        '''
        if self.room_exists(room_id):
            raise ValueError("Duplicated room_id name");
            # TODO: review irc, icq protocol to handle an eventual error message delivery
        self.rooms[room_id] = Room(session)
        
        
    def remove_room(self, room_id, session):
        ''' removes room from server's room pool
            Parameters
            ----------
            room_id : String
               represent the room id
               
            Return
            ------
                void
        '''
        if room_id == self.MAIN_ROOM_ID:
            raise UserWarning("You can't remove the main room")
        elif not self.rooms.get(room_id).has_moderator(session):
            raise UserWarning("You're not authorized to close this room")
        elif not self.rooms.get(room_id).is_empty:
            raise UserWarning("You can't close a non-empty room")
        else:
            room_obj = self.rooms.pop(room_id)
            del room_obj
    
    # room-session relation methods
    
    def is_session_in_room(self, session, room_id):
        ''' ask if the session is included in room members list
            Parameters
            ----------
            session : ConnectionHandler
               session.
               
            room_id : String
               represent the room ids
               
            Return
            ------
                boolean
        '''
        # indexed by room_id
        return self.rooms.get(room_id).has_member(session)
    
    
    def add_session_to_room(self, session, room_id):
        ''' add session to room members list
            Parameters
            ----------
            session : ConnectionHandler
               session.
               
            room_id : String
               represent the room id
               
            Return
            ------
                void
        '''
       
        # TODO: review irc, icq protocol to handle an eventual error message delivery
        self.rooms.get(room_id).add_memeber(session)
    
        
    def remove_session_from_room(self, session, room_id):
        ''' remove session from room members list
            Parameters
            ----------
            session : ConnectionHandler
               session.
               
            room_id : String
               represent the room id
               
            Return
            ------
                void
        '''
        
        self.rooms.get(room_id).remove_member(session)
    
        
    def is_session_room_moderator(self, session, room_id):
        ''' asks if the session is included in room moderators list
            Parameters
            ----------
            session : ConnectionHandler
               session.
               
            room_id : String
               represent the room id
               
            Return
            ------
                boolean
        '''
        # indexed by room_id
        return self.rooms.get(room_id).has_moderator(session)
        
    def add_session_to_room_moderators(self, session, room_id):
        ''' add session to room moderators list
            Parameters
            ----------
            session : ConnectionHandler
               session.
               
            room_id : String
               represent the room id
               
            Return
            ------
                void
        '''
        # TODO: review irc, icq protocol to handle an eventual error message delivery
        self.rooms.get(room_id).add_moderator(session)
 
        
    def remove_session_from_room_moderators(self, session, room_id):
        ''' remove session from room moderators list
            Parameters
            ----------
            session : ConnectionHandler
               session.
               
            room_id : String
               represent the room id
               
            Return
            ------
                void
        '''
        self.rooms.get(room_id).remove_moderator(session)
  
