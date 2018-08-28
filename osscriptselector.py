from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.completion import WordCompleter
from windowsscript import WindowsScript
from linuxscript import LinuxScript

class OsScriptSelector():

    def linux(self, host_config):
        script = LinuxScript()
        script.execute(host_config)
  
    def windows(self, host_config):
        script = WindowsScript()
        script.execute(host_config)

