#!/usr/bin/python
from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from inventoryParser import InventoryParser
import re

class YesNoValidator( Validator ):
    def validate( self, document ):
        answer = document.text.lower()

        if answer and not answer in ["y", "n"]:
            raise ValidationError( message='Please answer Yes or No!' )
            
class OSValidator( Validator ):
    def validate( self, document ):
        os = document.text.lower()
        if os and not os in ["linux", "windows"]:
            raise ValidationError( message='Please chose Linux or Windows!' )


class HostIdValidator( Validator ):
    def __init__( self, inventoryDir ):
        self.inventory = InventoryParser( inventoryDir )
        
    def validate( self, document ):
        hostId = document.text.lower()
        
        if ( not re.match("^[a-zA-Z][a-zA-Z0-9-]*$", hostId) or len(hostId) > 20 ):
            raise ValidationError(message='Must have from 1 to 20 characters of [a-z,A-Z,0-9,-] starting with [a-z,A-Z].')
        
        filename = self.inventory.getHostFile( hostId )
        if ( not filename is None ) :
            raise ValidationError(message="Host Identification already defined in '" + filename + "'.")




if __name__ == "__main__":

    host_identification = prompt('Host Identification: ', validator=HostIdValidator("inventories"))
    
