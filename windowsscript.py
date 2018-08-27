from __future__ import unicode_literals
from prompt_toolkit import prompt
import configparser
import validators
import inquirer
import yaml

class WindowsScript():
    
    def createInventory(self, host_config):
        inventory = configparser.RawConfigParser()
        
        inventory[host_config['id']] = { }
        
        # for some reason, just ansible_host is not accepted. Hence, we changed the key
        hostKey = host_config['id'].replace('-','_') + "_host ansible_host"
        inventory[host_config['id']][hostKey] = host_config['address']
        
        inventory[host_config['id'] + ":vars"] = { }
        
        inventory[host_config['id'] + ":vars"]["ansible_user"] = host_config['user']
        
        # despite the documentation states that we should use ansible_pass, just ansible_ssh_pass works
        inventory[host_config['id'] + ":vars"]["ansible_ssh_pass"] = host_config['pass']
        inventory[host_config['id'] + ":vars"]["ansible_connection"] = 'winrm'
        inventory[host_config['id'] + ":vars"]["ansible_winrm_transport"] = 'ntlm'
        inventory[host_config['id'] + ":vars"]["ansible_winrm_server_cert_validation"] = 'ignore'
        
        f = open('./inventories/' + host_config['id'] + '.inventory', 'w')
        inventory.write(f, space_around_delimiters=False)
      
    def createPlaybook(self, host_config):

        mainPlay = {}
        mainPlay['name'] = "Auto-generated Playbook for " + host_config['id']
        mainPlay['hosts'] = "{{ HOSTS }}"
        
        taskList = []
        
        taskInfo = {
            "name": "Print Host OS",
            "debug": 'msg="Selected OS -> {{ ansible_distribution }}; Major version -> {{ ansible_distribution_major_version}}"'
        }
        taskList.append(taskInfo)
        
        taskPackages = {
            "name": "Install OS pre-selected packages",
            "win_chocolatey": {
                "name": "{{ item }}",
                "state": "present"
            },
            "with_items": []
        }
        
        if ('packages' in host_config):
            taskPackages["with_items"] = host_config['packages']
            taskList.append(taskPackages)
        
        
        taskAdditional = {
            "name": "Install OS additional packages",
            "win_chocolatey": {
                "name": "{{ item }}",
                "state": "present"
            },
            "with_items": []
        }
            
        if ('additional_packages' in host_config):
            taskAdditional["with_items"] = host_config['additional_packages']
            taskList.append(taskAdditional)
        
        mainPlay['tasks'] = taskList
        
        f = open('./playbooks/' + host_config['id'] + '.yml', 'w')
        
        yaml.safe_dump([mainPlay], f, default_flow_style=False)


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
            additional = prompt('Install any additional package available in chocolatey? (y/n)', validator=validators.YesNoValidator())
            if (additional == 'n'):
                break
            
            packages.append(
                prompt('Package name (this will not be validated by this automation tool):')
            )
            
        return packages
          

    def execute(self, host_config):
        
        host_config['user'] = prompt('username: ', validator=validators.UsernameValidator())
        
        host_config['pass'] = prompt('password: ', is_password=True)
        
        print
        
        host_config[ 'packages' ] = self.selectPackages( host_config )
               
        host_config[ 'additional_packages' ] = self.additionalPackages()
        
        self.createInventory(host_config)
        self.createPlaybook(host_config)
        
        print 
        print "Successfully created entry for " + host_config['id']
        print
        
        
        
