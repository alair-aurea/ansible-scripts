import configparser

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
        inventory[host_config['id'] + ":vars"]["ansible_ssh_pass"] = host_config['pass']
        inventory[host_config['id'] + ":vars"]["ansible_connection"] = 'winrm'
        inventory[host_config['id'] + ":vars"]["ansible_winrm_transport"] = 'ntlm'
        inventory[host_config['id'] + ":vars"]["ansible_winrm_server_cert_validation"] = 'ignore'
        
        if (not inventoryDir[-1]  == '/'):
            inventoryDir = inventoryDir + '/'
        
        f = open(inventoryDir + host_config['id'] + '.inventory', 'w')
        inventory.write(f, space_around_delimiters=False)
