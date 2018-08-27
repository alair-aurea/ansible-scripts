#!/usr/bin/python
from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from osscriptselector import OsScriptSelector
import inquirer

import validators
import sys

if __name__ == "__main__":

    forceOverwrite = "--overwrite" in sys.argv

    host_config = {}

    print

    host_config['id'] = prompt('Host Identification: ', validator=validators.HostIdValidator("inventories", forceOverwrite))
  
    host_config['address'] = prompt('Host address: ', validator=validators.HostAddressValidator())
    
    print
    
    dev = ['Java', '.NET', 'C++']
    os = ['linux', 'windows']
    
    questions = [
        inquirer.List('dev',
            message="Development Environment",
            choices=dev,
        ),
        
        inquirer.List('os',
            message="Base Operating System",
            choices=os,
        ),
    ]
    
    answers = inquirer.prompt(questions)

    host_config['dev'] = answers['dev']
    
    host_type = answers['os']
    
    selector = OsScriptSelector()
    
    selectedOSScript = getattr(selector, host_type)
    
    selectedOSScript( host_config )
