from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.completion import WordCompleter
from windowsscript import WindowsScript

class OsScriptSelector():

    def linux(self, host_config):
        
        print "execute linux"
  
    def windows(self, host_config):
        script = WindowsScript()
        script.execute(host_config)
