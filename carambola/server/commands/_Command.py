'''
Created on 01/06/2013

@author: pablo
'''
from abc import abstractmethod

class Command(metaclass=ABCMeta):
    '''
    abstract command class
    '''
    INVALID_COMMAND_ARGUMENTS = "Invalid command arguments"
    
    _command = ""
    _kparams = []
    _handler = None
    
    @property
    def command (self):
        return self._command
    
    @command.setter
    def command (self, command):
        self._command = command
    
    @property
    def kparams (self):
        return self._kparams
    
    @kparams.setter
    def kparams (self, kparams):
        self._kparams = kparams
        
    @property
    def handler (self):
        return self._kparams
    
    @handler.setter
    def handler (self, handler):
        self._handler = handler

    def __init__(self, command, handler):
        ''' Constructor
            
            Parameters:
            ----------
            command :    String
                Specifies which command is being processed
            
            server : Server
                The listening server instance
        '''
        self.command = command
        self.handler = handler
    
    
    @abstractmethod
    def _parse_args(self, raw): pass
    
    @abstractmethod
    def _verify_request(self): pass
    
    @abstractmethod
    def _execute(self): pass
    
    
    def process(self, raw):
        ''' processes the command with the given arguments
            
            Parameters:
            ----------
            raw :    String
                String containing the raw arguments for the command. This string would 
                be parsed and verified before command execution
            
            Return
            ------
                void
                
            Raises
            ------
                UserWarning
        '''
        # template method
        
        self.kparams = self.parse_args(raw)
        
        if self.verify_request() :
            return self.execute()
        else:
            raise UserWarning(self.INVALID_COMMAND_ARGUMENTS)
        
    
