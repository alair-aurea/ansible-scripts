from __future__ import unicode_literals
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.completion import WordCompleter
from inventoryParser import InventoryParser
from enum import Enum

import re

class YesNoValidator( Validator ):
    def validate( self, document ):
        answer = document.text.lower()

        if answer and not answer in ["y", "n"]:
            raise ValidationError( message='Please answer Yes or No!' )


class HostIdValidator( Validator ):
    
    def __init__( self, inventoryDir, forceOverwrite ):
        self.inventory = InventoryParser( inventoryDir )
        self.reservedNames = "^(windows|ubuntu|amazon)(-.+)?-base$"
        self.forceOverwrite = forceOverwrite
        
    def validate( self, document ):
        hostId = document.text.lower()
        
        if ( not re.match("^[a-zA-Z][a-zA-Z0-9-_]{0,19}$", hostId)):
            raise ValidationError(message='Must have from 1 to 20 characters of [a-z,A-Z,0-9,-] starting with [a-z,A-Z].')
            
        if ( re.match(self.reservedNames, hostId) ):
            raise ValidationError(message='Reserved Name. Pattern: ' + self.reservedNames)
            
        filename = self.inventory.getHostFile( hostId )
        if ( not self.forceOverwrite and not filename is None ) :
            raise ValidationError(message="Host Identification already defined in '" + filename + "'. Use --overwrite to force.")


class HostAddressValidator( Validator ):
  
    def __init__( self ):
        self.validHostAddressRegex =  "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$";


    def validate( self, document ):
        hostAddress = document.text.lower()
        
        validAddress = re.match(self.validHostAddressRegex, hostAddress)
        
        if ( not validAddress ):
            raise ValidationError(message='Invalid hostname or IP address') 

class UsernameValidator( Validator ):
  
    def __init__( self ):
        self.validUsernameRegex = "^[a-zA-Z0-9_.-]+$"


    def validate( self, document ):
        username = document.text.lower()
        
        validUsername = re.match(self.validUsernameRegex, username)
        
        if ( not validUsername  ):
            raise ValidationError(message='Invalid username') 
            
