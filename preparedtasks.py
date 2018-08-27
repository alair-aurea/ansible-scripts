from __future__ import unicode_literals
from prompt_toolkit import prompt
from os import walk
import inquirer

class PreparedTasks():
    def __init__( self, preparedTasksDir ):
        self.preparedTasksDir = preparedTasksDir
            
    def getPlaybookFilenames( self ):
        for (dirpath, dirnames, filenames) in walk(self.preparedTasksDir):
            filenames = [ fi for fi in filenames if fi.endswith((".yml", ".yaml")) ]
            return filenames

    def selectTasks( self ):
      
        questions = [
            inquirer.List('task',
                  message="Select the playbook: ",
                  choices=self.getPlaybookFilenames(),
              ),
        ]
        
        return inquirer.prompt(questions)['task']
