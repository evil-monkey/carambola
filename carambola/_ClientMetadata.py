'''
Created on 02/06/2013

@author: pablo
'''

class ClientMetadata(object):
    '''
    Represents client metadata (non connection level) info
    '''

    _status = None  # TODO: define a class for status object
    _nickname = ""
    _email = ""
    _avatar = None  # placeholder for picture
    _tooltip_message = ""  # what I'm doing|thinking|eating... stuff

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status):
        self._status = status
        
    @property
    def nickname(self):
        return self._nickname
    
    @nickname.setter
    def nickname(self, nickname):
        self._nickname = nickname
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        self._email = email
        
    @property
    def avatar(self):
        return self.avatar
    
    @avatar.setter
    def avatar(self, avatar):
        self._avatar = avatar
        
    @property
    def tooltip_message(self):
        return self._tooltip_message
    
    @tooltip_message.setter
    def tooltip_message(self, tooltip_message):
        self._tooltip_message = tooltip_message
        

    def __init__(self):
        pass
