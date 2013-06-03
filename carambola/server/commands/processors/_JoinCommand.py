'''
Created on 02/06/2013

@author: pablo
'''
from carambola.server.commands._Command import Command

class JoinCommand(Command):
    '''
    Join command processor
    '''


    def __init__(self, command, server):
        ''' Constructor
            
            Parameters:
            ----------
            command :    String
                Specifies which command is being processed
            
            server : Server
                The listening server instance
        '''
        super(JoinCommand, self).__init__(command)
        
    def _parse_args(self, raw):
        return [raw.strip(' \t\n\r')]
    
    def _verify_request(self):
        if not self._kparams or not self.kparams[0].startswith("#"):
            return False
    
        
        
        
