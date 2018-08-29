from __future__ import unicode_literals

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


 
