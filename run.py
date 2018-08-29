#!/usr/bin/python

from ansible_scripts import *

if __name__ == "__main__":
    autoConfig = AutoConfig()
    try:
        autoConfig.run()
    except ( TypeError, KeyboardInterrupt ) as e:
        pass
