#!/usr/bin/python
from inventoryParser import InventoryParser
from ansibleproxy import AnsibleProxy
from ansiblesetup import AnsibleSetup
import inquirer
import constants


def runPreconfiguredHost( host ):
    ansibleProxy = AnsibleProxy(constants.INVENTORIES_DIR, constants.PLAYBOOKS_DIR)
    ansibleProxy.run( host )
    
def configureNewHost( ):
    ansibleSetup = AnsibleSetup()
    ansibleSetup.run()


if __name__ == "__main__":

    inventoryParser = InventoryParser( constants.INVENTORIES_DIR )
    
    menuOptions=inventoryParser.getAllHosts()
    menuOptions.append( constants.CREATE_NEW_HOST_TEXT )
    
    print
    
    questions = [
        inquirer.List( 'inventory',
            message=constants.SELECT_OR_CREATE_HOST_TEXT,
            choices=menuOptions,
        ),
    ]
    
    answers = inquirer.prompt( questions )
    
    if( answers['inventory'] == constants.CREATE_NEW_HOST_TEXT):
        configureNewHost()
    else:
        runPreconfiguredHost( answers[ 'inventory' ] )
        
    
