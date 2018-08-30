from __future__ import unicode_literals
from subprocess import call
from inventoryParser import InventoryParser
import time

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
            start_time = time.time()
            call(["ansible-playbook", "-i", hostfile, "-e HOSTS=" + host, "playbooks/"+ host +".yml"])
            elapsed_time = time.time() - start_time
            print "Elapsed time:", "{:10.2f}".format(elapsed_time), "seconds"
            print

