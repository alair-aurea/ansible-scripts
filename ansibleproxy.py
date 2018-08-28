from __future__ import unicode_literals
from subprocess import call
from inventoryParser import InventoryParser

class AnsibleProxy():
    def __init__(self, inventoryDir, playbooksDir):
        self.invetoryDir = inventoryDir
        self.playbooksDir = playbooksDir
  
    def run(self, host):
        inventory = InventoryParser(self.invetoryDir);
        hostfile = inventory.getHostFile(host)
        if (hostfile is None):
            raise ValueError('Given host does not exist.') 
        else:
            call(["ansible-playbook", "-i", hostfile, "-e HOSTS=" + host, "playbooks/"+ host +".yml"])
