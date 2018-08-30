from __future__ import unicode_literals
import configparser
import inquirer
import validators
import constants

class PackageHandler():

    def __init__( self, config_file ):
        self.config_file = config_file
        self.repository = 'package'

    def selectPackages( self, host_config ):
        base_config = configparser.RawConfigParser(allow_no_value=True)
        base_config.read( self.config_file )
        
        packages = []
        default = []
        
        config = dict( base_config.items( host_config['distro'] + ':' + host_config['dev'] + ":" + self.repository ) )
        
        for package in config.keys(): 
            packages.append(package)
            if (config[package] == 'yes'):
                default.append(package)
        if ( len( packages ) > 0 ):
              questions = [
                  inquirer.Checkbox('packages',
                      message=constants.PACKAGES_TEXT,
                      choices=packages,
                      default=default
                  ),
              ]
              answers = inquirer.prompt(questions)            
              return answers[ 'packages' ]
        else:
            configFile = constants.CONFIGS_DIR + '/' + host_config['os'] + constants.CONFIG_FILE_EXTENSION
            print constants.NO_PACKAGES_AVAILABLE_TEXT + ' in ' + configFile + '. Skipping package selection.'
            print
            return []

    def selectAdditionalPackages( self ):
      
        packages = []
        while(True):
            additional = inquirer.prompt([
                        inquirer.Confirm('additional',
                            message=constants.INSTALL_ADDITIONAL_PACKAGES_TEXT,
                            default=False,
                        ),
                    ])['additional']
            if (not additional):
                break
            
            package = inquirer.prompt([
                        inquirer.Text('package',
                            message=constants.ADDITIONAL_PACKAGES_TEXT
                        ),
                    ])['package']
            
            packages.append( package )
            print
            
        return packages
