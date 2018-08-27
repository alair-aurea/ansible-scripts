#!/usr/bin/python

import configparser
from os import walk
import configparser

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
        for (dirpath, dirnames, filenames) in walk(self.invetoryDir):
            filenames = [ dirpath + "/" + fi for fi in filenames if fi.endswith(".inventory") ]
            return filenames
        
    def getInventories( self ):
        return self.configs.keys()
        
    def getHostFile(self, host):
        for inventory in self.getInventories():
            if (host in self.configs[inventory].keys() ):
                return inventory
        return None;
        
    def hostExists(host):
        return not self.getHostFile(host) is None
