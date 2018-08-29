#!/usr/bin/python

import configparser
from os import walk
import configparser
import constants

class InventoryParser():
    def __init__(self, inventoryDir):
        self.invetoryDir = inventoryDir
        filenames = self.getInventoryFilenames()
        self.configs = {}
        for filename in filenames:
            config = configparser.RawConfigParser()
            config.read(filename)
            self.configs[filename] = config
            
    def getInventoryFilenames( self ):
        filenames = []
        for (dirpath, dirnames, filenames) in walk(self.invetoryDir):
            filenames = [ dirpath + "/" + fi for fi in filenames if fi.endswith(constants.INVENTORY_EXTENSION) ]
            break
        return filenames
        
    def getInventories( self ):
        return self.configs.keys()
    
    def getAllHosts( self ):
        hosts = []
        for inventory in self.getInventories():
            hosts.extend([host for host in self.configs[inventory].keys() 
                                    if not host.endswith(":vars") and not host == 'DEFAULT'])
        return hosts
    
    
    def getHostFile(self, host):
        for inventory in self.getInventories():
            if (host in self.configs[inventory].keys() ):
                return inventory
        return None;
        
    def hostExists( self, host ):
        return not self.getHostFile(host) is None
