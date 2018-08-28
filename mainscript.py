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




class MainScript():

    def __init__( self, host_config  ):
        self.host_config = host_config
        
    def selectDistro( self ):
        host_config = self.host_config
        
        if (host_config['os'] == 'windows'):
            return 'windows'
      
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read('configs/linux.conf')
        
        questions = [
            inquirer.List('distro',
                  message="Select one distro",
                  choices=config['distros'],
              ),
        ]
        
        return inquirer.prompt(questions)['distro']
        

    def execute( self ):
        
        host_config = self.host_config
        
        host_config['user'] = prompt('username: ', validator=validators.UsernameValidator())
        
        print
        
        usesKey = prompt('Connect using Key File? (y/N): ', validator=validators.YesNoValidator()).lower()
        
        if ( usesKey == 'y' ):
            fileSelector = FileSelector("keys/", (".pem", ".ppk"), "Select the key file")
            keyFile = fileSelector.select()
            
            if (keyFile):
                host_config['key-file'] = keyFile
                host_config['security'] = 'key'
            else:
                print "[Error] No available keys. Place the key files in the 'keys' directory and run again. Falling back to password."
                usesKey = 'n'
                
        
        if ( usesKey == 'n' or usesKey == '' ):
            host_config['security'] = 'pass'
            host_config['pass'] = prompt('password: ', is_password=True)

        print
        
        
        try:
            host_config['distro'] = self.selectDistro()
        except:
            print "[Error] Cannot load configs. Do the config files exist? Correct the error and run again."
            return
            
        wantsPre = prompt('Execute preparation tasks? (y/N): ', validator=validators.YesNoValidator()).lower()
        
        if ( wantsPre == 'y' ):
            fileSelector = FileSelector("prepared-tasks/", (".yml", ".yaml"), "Select the preparation tasks file")
            taskFile = fileSelector.select()
            if ( taskFile ):
                host_config['pre-tasks'] = "prepared-tasks/" + taskFile
            else: 
                print
                print "[Error] No prepared tasks available. Place prepared playbooks in 'prepared-tasks' directory and run again."
                print
        
        configFile = "configs/" + host_config['os'] + ".conf"
        
        packageHandler = PackageHandler(configFile)
        
        try:
            host_config[ 'packages' ] = packageHandler.selectPackages( host_config )
            host_config[ 'additional_packages' ] = packageHandler.selectAdditionalPackages()
        except:
            print "[Error] Cannot load configs. Do the config files exist? Correct the error and run again."
            return
        
        inventory_creator = InventoryCreator()
        inventory_creator.create(host_config, "./inventories")
        
        print
        
        wantsPost = prompt('Execute Post-installation tasks? (y/N): ', validator=validators.YesNoValidator()).lower()
        
        if ( wantsPost == 'y' ):
            fileSelector = FileSelector("prepared-tasks/", (".yml", ".yaml"), "Select the post-installation tasks file")
            taskFile = fileSelector.select()
            if (taskFile):
                host_config['post-tasks'] = "prepared-tasks/" + taskFile
            else: 
                print
                print "[Error] No prepared tasks available. Place prepared playbooks in 'prepared-tasks' directory and run again."
                print
        
        playbook_creator = PlaybookCreator()
        playbook_creator.create(host_config, "./playbooks")
        
        print 
        print "Successfully created entry for " + host_config['id']
        print
        
        
      
