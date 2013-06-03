'''
Created on 02/06/2013

@author: pablo
'''

class Room(object):
    '''
    Class representing a channel
    '''
    DUPLICATED_MEMBER = "Duplicated member session"
    DUPLICATED_MODERATOR = "Duplicated moderator session"
            
    _room_id = ""
    _private = True
    _members = []
    _moderators = []
    _created_by = ""
    _last_message_by = ""
    _last_message_timestamp = ""
    _topic = ""
    _welcome_message = "{nickname} has joined this room. Welcome {nickname} to #{room_id}.\r\n"
    _server = None
    
    @property
    def room_id(self):
        return self._room_id
    
    @room_id.setter
    def room_id(self, room_id):
        self._room_id = room_id
        
    @property
    def is_private(self):
        return self._private
    
    @is_private.setter
    def is_private(self, private):
        self._private = private
        
    @property
    def members(self):
        return self._members
    
    @members.setter
    def members(self, members):
        self._members = members
        
    @property
    def moderators(self):
        return self._moderators
    
    @moderators.setter
    def moderators(self, moderators):
        self._moderators = moderators
        
    @property
    def created_by(self):
        return self._created_by
    
    @created_by.setter
    def created_by(self, created_by):
        self._created_by = created_by
        
    @property
    def last_message_by(self):
        return self._last_message_by
    
    @last_message_by.setter
    def last_message_by(self, last_message_by):
        self._last_message_by = last_message_by
        
    @property
    def last_message_timestamp(self):
        return self._last_message_timestamp
    
    @last_message_by.setter
    def last_message_by(self, last_message_timestamp):
        self._last_message_timestamp = last_message_timestamp
        
    @property
    def topic(self):
        return self._topic
    
    @topic.setter
    def topic(self, topic):
        self._topic = topic
        
    @property
    def welcome_message(self):
        return self._welcome_message
    
    @welcome_message.setter
    def welcome_message(self, welcome_message):
        self._welcome_message = welcome_message


    def __init__(self, server, creator=None):
        ''' Constructor
            
            Parameters:
            ----------
                creator: ConnectionHandler
                    client who's creating the channel
        '''
        self._server = server
        
        if creator is not None:
            self.members.append(creator)
            self.moderators.append(creator)
            self.created_by(creator.metadata.nickname)
    
    
    def has_member(self, session):
        return self.members.count(session) > 0
    
    def has_moderator(self, session):
        return self.moderators.count(session) > 0
    
    def add_member(self, session):
        if self.has_member(session):
            raise ValueError(self.DUPLICATED_MEMBER);
        
        as_moderator = self.is_empty
            
        self.members.append(session)
        
        message = self.welcome_message.format(
            nickname=session.metadata.nickname ,
            room_id=self.room_id)
        self.broadcast(message)
                
        if as_moderator:
            self.add_moderator(session)
        
        
    def add_moderator(self, session):
        if self.has_moderator(session):
            raise ValueError(self.DUPLICATED_MODERATOR);
        
        self.moderators.append(session)
        
    def remove_member(self, session):
        self.members.remove(session)
        
    def remove_moderator(self, session):
        self.moderators.remove(session)
        
    def is_empty(self):
        return not self.members
    
    def broadcast(self, message, sender=None):
        
        from_nickname = ""
        if sender is not None:
            from_nickname = sender.metadata.nickname
        else:
            from_nickname = "#" + self.room_id
            
        message = "{0}> {1}".format(from_nickname, message)
        
        for session in self.members :
            if not session.equals(sender):
                session.say(message)
       
        
    
    
