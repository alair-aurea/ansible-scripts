from __future__ import unicode_literals
from prompt_toolkit import prompt
from windowsinventorycreator import InventoryCreator
from windowsplaybookcreator import PlaybookCreator
import configparser
import validators
import inquirer
import yaml

class WindowsScript():

    def selectPackages( self, host_config ):
        base_config = configparser.RawConfigParser(allow_no_value=True)
        base_config.read( "configs/windows.conf" )
        
        packages = []
        default = []
        
        config = dict(base_config.items('chocolatey:' + host_config['dev']))
        
        for package in config.keys(): 
            packages.append(package)
            if (config[package] == 'yes'):
                default.append(package)
                print
            
        
        questions = [
            inquirer.Checkbox('packages',
                message="Which packages do you want to install?",
                choices=packages,
                default=default
            ),
        ]
        answers = inquirer.prompt(questions)
        
        return answers[ 'packages' ]

    def additionalPackages( self ):
      
        packages = []
        while(True):
            additional = prompt('Install any additional package available in chocolatey? (y/n): ', validator=validators.YesNoValidator())
            if (additional == 'n'):
                break
            
            packages.append(
                prompt('Package name (this will not be validated by this automation tool): ')
            )
            
        return packages
          

    def execute(self, host_config):
        
        host_config['user'] = prompt('username: ', validator=validators.UsernameValidator())
        
        host_config['pass'] = prompt('password: ', is_password=True)
        
        print
        
        host_config[ 'packages' ] = self.selectPackages( host_config )
               
        host_config[ 'additional_packages' ] = self.additionalPackages()
        
        inventory_creator = InventoryCreator()
        inventory_creator.create(host_config, "./inventories")
        
        playbook_creator = PlaybookCreator()
        playbook_creator.create(host_config, "./playbooks")
        
        print 
        print "Successfully created entry for " + host_config['id']
        print
        
        
        
