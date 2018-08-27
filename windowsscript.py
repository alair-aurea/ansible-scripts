from __future__ import unicode_literals
from prompt_toolkit import prompt
from windowsinventorycreator import InventoryCreator
from windowsplaybookcreator import PlaybookCreator
from packagehandler import PackageHandler
import configparser
import validators
import inquirer
import yaml

class WindowsScript():         

    def execute(self, host_config):
        
        host_config['user'] = prompt('username: ', validator=validators.UsernameValidator())
        
        host_config['pass'] = prompt('password: ', is_password=True)
        
        print
        
        host_config['distro'] = 'windows' # windows is considered just one distro
        
        packageHandler = PackageHandler("configs/windows.conf", "chocolatey")
        
        host_config[ 'packages' ] = packageHandler.selectPackages( host_config )
               
        host_config[ 'additional_packages' ] = packageHandler.selectAdditionalPackages()
        
        inventory_creator = InventoryCreator()
        inventory_creator.create(host_config, "./inventories")
        
        playbook_creator = PlaybookCreator()
        playbook_creator.create(host_config, "./playbooks")
        
        print 
        print "Successfully created entry for " + host_config['id']
        print
        
        
        
