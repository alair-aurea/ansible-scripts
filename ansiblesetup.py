#!/usr/bin/python
from __future__ import unicode_literals
from inventoryParser import InventoryParser
from fileselector import FileSelector
from playbookcreator import PlaybookCreator
from inventorycreator import InventoryCreator
from packagehandler import PackageHandler
import inquirer
import constants
import configparser


import validators
import sys

class AnsibleSetup():
    
    def run( self ):
        host_config = {}

        host_config['id'] = self.askHostId()
        
        env = self.askEnvQuestions()
        host_config['address'] = env['hostaddress']
        host_config['dev'] = env['dev']     
        host_config['os'] = env['os']
        
        host_config['user'] = self.askUsername()
        print
        
        usekey = self.askUseKeySecurity()
        
        while( usekey ):
            fileSelector = FileSelector(constants.KEY_FILES_DIR, (".pem", ".ppk"), constants.KEY_FILE_TEXT)
            keyFile = fileSelector.select()
            if ( not keyFile ):
                print constants.NO_KEY_AVAILABLE                
                print
                usekey = not self.askFallbackToPass()
            else:
                host_config['key-file'] = keyFile
                host_config['security'] = 'key'
                break
        
        if ( not usekey ):
            host_config['security'] = 'pass'
            host_config['pass'] = self.askPass()
        
        
        
        host_config['distro'] = self.askDistro( host_config )
        
        usePreTask = self.askUsePreparationTaskFile()
        if ( usePreTask ):
            fileSelector = FileSelector(constants.PREPARED_TASKS_DIR, (".yml", ".yaml"), constants.PREPARATION_TASK_FILE_TEXT)
            taskFile = fileSelector.select()
            if (taskFile):
                host_config['pre-tasks'] = constants.PREPARED_TASKS_DIR + "/" + taskFile
            else: 
                print
                print "[Error] No prepared tasks available. Place prepared playbooks in '" + constants.PREPARED_TASKS_DIR +"' directory and run again."
                print
        
        print 
        
        configFile = "configs/" + host_config['os'] + ".conf"
        
        packageHandler = PackageHandler(configFile)
        
        host_config[ 'packages' ] = packageHandler.selectPackages( host_config )
        host_config[ 'additional_packages' ] = packageHandler.selectAdditionalPackages()
        
        print
        
        usePostTask = self.askUsePostInstallTaskFile()
        if ( usePostTask ):
            fileSelector = FileSelector(constants.PREPARED_TASKS_DIR, (".yml", ".yaml"), constants.POST_INSTALLATION_TASK_FILE_TEXT)
            taskFile = fileSelector.select()
            if (taskFile):
                host_config['post-tasks'] = constants.PREPARED_TASKS_DIR + "/" + taskFile
            else: 
                print
                print "[Error] No prepared tasks available. Place prepared playbooks in '" + constants.PREPARED_TASKS_DIR +"' directory and run again."
                print
                
        inventory_creator = InventoryCreator()
        inventory_creator.create(host_config, constants.INVENTORIES_DIR)
        
        playbook_creator = PlaybookCreator()
        playbook_creator.create(host_config, constants.PLAYBOOKS_DIR)
        
        print 
        print "Successfully created entry for " + host_config['id']
        print
  
  
  
    def getHostIdQuestion( self ):
        return inquirer.Text('hostid',
                    constants.HOST_IDENTIFICATION_TEXT,
                    validate=validators.hostIdValidate 
                )
  
    def getOverwriteQuestion( self, filename ):
        return inquirer.Confirm('overwrite',
                    message=constants.FILE_OVERWRITE_TEXT + " '" + filename + "'",
                    default=False
                )
  
    def askHostId( self ):
        while( True ):
            questions = [
                self.getHostIdQuestion( ),
            ]
            hostId = inquirer.prompt( questions )['hostid']
            inventory = InventoryParser( constants.INVENTORIES_DIR )
            filename = inventory.getHostFile( hostId )
            if ( filename is None ) :
                return hostId
            else:
                print
                print "Selected Host Id already defined in '" + filename + "'!"
                questions = [
                    self.getOverwriteQuestion( filename ),
                ]
                overwrite = inquirer.prompt( questions ) ['overwrite']
                if ( overwrite ):
                    return hostId
                else:
                    print
    
    def getHostAddressQuestion( self ):
        return inquirer.Text('hostaddress',
                    constants.HOST_ADDRESS_TEXT,
                    validate=validators.hostAddressValidate 
                )
                
                
    def getDevEnvQuestion( self ):
        return inquirer.List('dev',
                    message=constants.DEVELOPMENT_ENV_TEXT,
                    choices=['Java', '.NET', 'C++'],
                )
                
    def getOSQuestion( self ):
        return inquirer.List('os',
                    message=constants.BASE_OS_TEXT,
                    choices=['linux', 'windows'],
                )

    def askEnvQuestions( self ):
        questions = [
            self.getHostAddressQuestion(),
            self.getDevEnvQuestion(),
            self.getOSQuestion(),
        ]
      
        return inquirer.prompt(questions)

  
    def askUsername( self ):
        return inquirer.prompt([
                inquirer.Text('username',
                    constants.USERNAME_TEXT,
                    validate=validators.usernameValidate 
                )
            ])['username']
        
        
    def askUseKeySecurity( self ):
        return inquirer.prompt([
                inquirer.Confirm('key-security',
                    message=constants.USE_KEY_FILE_TEXT,
                    default=True
                )
            ])['key-security']


    def getPassQuestion( self ):
        return inquirer.Password('password',
                    message=constants.PASSWORD_TEXT
                )

    def askPass( self ):
        questions = [
            self.getPassQuestion(),
        ]
        return inquirer.prompt(questions)['password']


    def getUsePreparationTasks( self ):
        return inquirer.Confirm('pre-tasks',
                    message=constants.USE_PREPARATION_TASK_FILE_TEXT,
                    default=True
                )
    
    def getUsePostInstallationTasks( self ):
        return inquirer.Confirm('post-tasks',
                    message=constants.USE_POST_INSTALLATION_TASK_FILE_TEXT,
                    default=True
                )
                
    def askUsePreparationTaskFile( self ):
        questions = [
            self.getUsePreparationTasks(),
        ]
        return inquirer.prompt(questions)['pre-tasks']
        
    def askUsePostInstallTaskFile( self ):
        questions = [
            self.getUsePostInstallationTasks(),
        ]
        return inquirer.prompt(questions)['post-tasks']
        
    def askDistro( self, host_config ):
        
        if (host_config['os'] == 'windows'):
            return 'windows'
      
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read(constants.CONFIGS_DIR + '/linux.conf')
        
        questions = [
            inquirer.List('distro',
                  message="Select one distro",
                  choices=config['distros'],
              ),
        ]
        
        return inquirer.prompt(questions)['distro']

    def askFallbackToPass( self ):
        return inquirer.prompt([
                inquirer.List('fallback-to-pass',
                    message=constants.SELECT_ACTION,
                    choices= [constants.ADD_KEY_AND_RETRY, constants.FALLBACK_TO_PASS]
                )
            ])['fallback-to-pass'] == constants.FALLBACK_TO_PASS
