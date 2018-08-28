from __future__ import unicode_literals
from prompt_toolkit import prompt
import configparser
import inquirer
import validators

class PackageHandler():

    def __init__( self, config_file ):
        self.config_file = config_file
        self.repository = 'package'

    def selectPackages( self, host_config ):
        base_config = configparser.RawConfigParser(allow_no_value=True)
        base_config.read( self.config_file )
        
        packages = []
        default = []
        
        config = dict(base_config.items( host_config['distro'] + ':' + host_config['dev'] + ":" + self.repository) )
        
        for package in config.keys(): 
            packages.append(package)
            if (config[package] == 'yes'):
                default.append(package)
        
        questions = [
            inquirer.Checkbox('packages',
                message="Which packages do you want to install?",
                choices=packages,
                default=default
            ),
        ]
        answers = inquirer.prompt(questions)
        
        return answers[ 'packages' ]

    def selectAdditionalPackages( self ):
      
        packages = []
        while(True):
            additional = prompt('Install any additional package available in ' + self.repository + '? (y/N): ', validator=validators.YesNoValidator()).lower()
            if (not additional == 'y'):
                break
            
            packages.append(
                prompt('Package name (this will not be validated by this automation tool): ')
            )
            print
            
        return packages
