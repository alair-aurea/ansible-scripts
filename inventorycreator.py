import configparser
import constants
import os

class InventoryCreator():
    def create(self, host_config, inventoryDir):
        inventory = configparser.RawConfigParser()
        
        inventory[host_config['id']] = { }
        
        # for some reason, just ansible_host is not accepted. Hence, we changed the key
        hostKey = host_config['id'].replace('-','_') + "_host ansible_host"
        inventory[host_config['id']][hostKey] = host_config['address']
        
        inventory[host_config['id'] + ":vars"] = { }
        
        inventory[host_config['id'] + ":vars"]["ansible_user"] = host_config['user']
        
        # despite the documentation states that we should use ansible_pass, just ansible_ssh_pass works
        if ( host_config['security'] == 'pass'):
            inventory[host_config['id'] + ":vars"]["ansible_ssh_pass"] = host_config['pass']
        else:
            inventory[host_config['id'] + ":vars"]["ansible_ssh_private_key_file"] = "{{ inventory_dir }}/../keys/" + host_config['key-file']
        
        
        if (host_config['os'] == 'windows'):
            inventory[host_config['id'] + ":vars"]["ansible_connection"] = 'winrm'
            inventory[host_config['id'] + ":vars"]["ansible_winrm_transport"] = 'ntlm'
            inventory[host_config['id'] + ":vars"]["ansible_winrm_server_cert_validation"] = 'ignore'
        else:
            inventory[host_config['id'] + ":vars"]["ansible_connection"] = 'ssh'
        
        
        # copy additional variables from config
        configFile = constants.CONFIGS_DIR + '/' + host_config['os'] + constants.CONFIG_FILE_EXTENSION
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read(configFile)
        section = host_config['distro'] + ':ansible:variables'
        
        if ( section in config.keys() ):
          for ( key, val ) in config[section].items():
              inventory[host_config['id'] + ":vars"][key] = val
        
        
        if (not inventoryDir[-1]  == '/'):
            inventoryDir = inventoryDir + '/'
        
        if not os.path.exists(inventoryDir):
            os.makedirs(inventoryDir)
        
        f = open(inventoryDir + host_config['id'] + constants.INVENTORY_EXTENSION, 'w')
        inventory.write(f, space_around_delimiters=False)
