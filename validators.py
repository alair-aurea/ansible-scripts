from __future__ import unicode_literals
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.completion import WordCompleter
from inventoryParser import InventoryParser
from enum import Enum

import re


def hostIdValidate( answers, current ):
    if ( not re.match("^[a-zA-Z][a-zA-Z0-9-_]{0,19}$", current)):
        return False
    
    return True

def hostAddressValidate( answers, current ):
    if ( not re.match("^((([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])){1,}$", current)):
        return False
    
    return True

def usernameValidate( answers, current ):
    if ( not re.match("^[a-zA-Z0-9_.-]+$", current)):
        return False
    
    return True


class YesNoValidator( Validator ):
    def validate( self, document ):
        answer = document.text.lower()

        if answer and not answer in ["y", "n"]:
            raise ValidationError( message='Please answer Yes or No!' )

 
