from __future__ import unicode_literals
from prompt_toolkit import prompt
from subprocess import call
from os import walk

import sys
import configparser
from inventoryParser import InventoryParser

def printUsage():
    print
    print "    Usage:", sys.argv[0], "host_identification"
    print

def printHowToSetup(host):
    print
    print "    No configuration found for host '" + host + "'. Run ansible-setup.py to create a new configuration'."
    print


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        printUsage();
    else:
        inventory = InventoryParser("./inventories");
        host = sys.argv[1]
        hostfile = inventory.getHostFile(host)
        if (hostfile is None):
            printHowToSetup(host)
        else:
            call(["ansible-playbook", "-i", hostfile, "-e HOSTS=" + host, "playbooks/base.yml"])
