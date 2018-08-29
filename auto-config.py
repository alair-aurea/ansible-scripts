#!/usr/bin/python
from inventoryParser import InventoryParser
from ansibleproxy import AnsibleProxy
from ansiblesetup import AnsibleSetup
import inquirer
import constants
import os

def runPreconfiguredHost( host ):
    ansibleProxy = AnsibleProxy(constants.INVENTORIES_DIR, constants.PLAYBOOKS_DIR)
    ansibleProxy.run( host )
    
def configureNewHost( ):
    ansibleSetup = AnsibleSetup()
    ansibleSetup.run()

def deleteHost( hostList ): 
    host = inquirer.prompt([
          inquirer.List( 'host',
                  message=constants.SELECT_HOST_TO_DELETE_TEXT,
                  choices=hostList,
              ),
        ])['host']
        
    delete = inquirer.prompt([
          inquirer.Confirm( 'confirmation',
                  message='Delete ' + host,
                  default=False,
              ),
        ])['confirmation']
        
    if ( delete ):
        os.remove(constants.INVENTORIES_DIR + '/' + host + constants.INVENTORY_EXTENSION)
        os.remove(constants.PLAYBOOKS_DIR + '/' + host + constants.PLAYBOOK_FILE_EXTENSION)
        print
        print constants.HOST_DELETED_TEXT
        print
    else:
        print
        print constants.CANCELED_BY_USER_TEXT
        print


if __name__ == "__main__":

    inventoryParser = InventoryParser( constants.INVENTORIES_DIR )
    
    hostList = inventoryParser.getAllHosts()
    
    menuOptions = ['Run ' + s for s in hostList]
    
    menuOptions.append( constants.CREATE_NEW_HOST_TEXT )
    
    if ( len(hostList) > 0 ):
        menuOptions.append( constants.DELETE_HOST_TEXT )
    
    print
    
    action = inquirer.prompt([
          inquirer.List( 'action',
                  message=constants.SELECT_ACTION,
                  choices=menuOptions,
              ),
        ])['action']
    
    if( action == constants.CREATE_NEW_HOST_TEXT ):
        configureNewHost()
    elif ( action == constants.DELETE_HOST_TEXT ):
            deleteHost( hostList )
    else:
        runPreconfiguredHost( action.split()[1] )
        
    
