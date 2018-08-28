from __future__ import unicode_literals
from prompt_toolkit import prompt
from inventorycreator import InventoryCreator
from playbookcreator import PlaybookCreator
from packagehandler import PackageHandler
from fileselector import FileSelector
import configparser
import validators
import inquirer
import yaml

class WindowsScript():         

    def execute(self, host_config):
        
        host_config['user'] = prompt('username: ', validator=validators.UsernameValidator())
        
        usesKey = prompt('Connect using Key File? (y/n): ', validator=validators.YesNoValidator())
        
        if ( usesKey == 'n' ):
            host_config['security'] = 'pass'
            host_config['pass'] = prompt('password: ', is_password=True)
        else:
            fileSelector = FileSelector("keys/", (".pem", ".ppk"), "Select the key file")
            host_config['security'] = 'key'
            host_config['key-file'] = fileSelector.select()
        
        print
        
        host_config['distro'] = 'windows' # windows is considered just one distro
        
        wantsPre = prompt('Execute preparation tasks? (y/n): ', validator=validators.YesNoValidator())
        
        if (wantsPre == 'y'):
            fileSelector = FileSelector("prepared-tasks/", (".yml", ".yaml"), "Select the preparation tasks file")
            taskfile = fileSelector.select()
            if (not taskfile is None):
                host_config['pre-tasks'] = "prepared-tasks/" + taskfile
        
        packageHandler = PackageHandler("configs/windows.conf", "chocolatey")
        
        host_config[ 'packages' ] = packageHandler.selectPackages( host_config )
               
        host_config[ 'additional_packages' ] = packageHandler.selectAdditionalPackages()
        
        inventory_creator = InventoryCreator()
        inventory_creator.create(host_config, "./inventories")
        
        print
        
        wantsPost = prompt('Execute Post-installation tasks? (y/n): ', validator=validators.YesNoValidator())
        
        if (wantsPost == 'y'):
            fileSelector = FileSelector("prepared-tasks/", (".yml", ".yaml"), "Select the post-installation tasks file")
            taskfile = fileSelector.select()
            if (not taskfile is None):
                host_config['post-tasks'] = "prepared-tasks/" + taskfile
        
        playbook_creator = PlaybookCreator()
        playbook_creator.create(host_config, "./playbooks")
        
        print 
        print "Successfully created entry for " + host_config['id']
        print
        
        
        
