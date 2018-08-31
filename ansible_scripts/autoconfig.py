#!/usr/bin/python
import os
from inventoryParser import InventoryParser
from ansibleproxy import AnsibleProxy
from ansiblesetup import AnsibleSetup
import inquirer
import constants


class AutoConfig():

    def runPreconfiguredHost( self, host ):
        ansibleProxy = AnsibleProxy(constants.INVENTORIES_DIR, constants.PLAYBOOKS_DIR)
        ansibleProxy.run( host )
        
    def configureNewHost( self ):
        ansibleSetup = AnsibleSetup()
        ansibleSetup.run()

    def deleteHost( self, hostList ): 
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


    def run( self ):

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
            self.configureNewHost()
        elif ( action == constants.DELETE_HOST_TEXT ):
            self.deleteHost( hostList )
        else:
            self.runPreconfiguredHost( action.split()[1] )
            
        
